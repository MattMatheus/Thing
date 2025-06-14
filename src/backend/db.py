from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

def get_graph_driver():
    return GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# Capsule CRUD (Graph)
def create_capsule(name, description, created_at):
    with get_graph_driver() as driver:
        with driver.session() as session:
            result = session.run(
                """
                CREATE (c:Capsule {id: randomUUID(), name: $name, description: $description, created_at: $created_at})
                RETURN c.id AS id
                """,
                name=name, description=description, created_at=created_at.isoformat()
            )
            return result.single()["id"]

def get_all_capsules():
    with get_graph_driver() as driver:
        with driver.session() as session:
            result = session.run("MATCH (c:Capsule) RETURN c")
            return [record["c"] for record in result]

def get_capsule_by_id(capsule_id):
    with get_graph_driver() as driver:
        with driver.session() as session:
            result = session.run("MATCH (c:Capsule {id: $capsule_id}) RETURN c", capsule_id=capsule_id)
            record = result.single()
            return dict(record["c"] if record else {}) if record else None

def delete_capsule(capsule_id):
    with get_graph_driver() as driver:
        with driver.session() as session:
            session.run(
                "MATCH (c:Capsule {id: $id}) DELETE c",
                id=capsule_id
            )

# Thread CRUD (Graph)
def create_thread(capsule_id, name, tags, created_at):
    with get_graph_driver() as driver:
        with driver.session() as session:
            result = session.run(
                """
                MATCH (c:Capsule {id: $capsule_id})
                CREATE (t:Thread {id: randomUUID(), name: $name, tags: $tags, created_at: $created_at})
                CREATE (c)-[:HAS_THREAD]->(t)
                RETURN t.id AS id
                """,
                capsule_id=capsule_id, name=name, tags=tags, created_at=created_at.isoformat()
            )
            return result.single()["id"]

def get_threads_by_capsule(capsule_id):
    with get_graph_driver() as driver:
        with driver.session() as session:
            result = session.run(
                """
                MATCH (c:Capsule {id: $capsule_id})-[:HAS_THREAD]->(t:Thread)
                RETURN t
                """,
                capsule_id=capsule_id
            )
            return [record["t"] for record in result]

def get_thread_by_id(thread_id):
    with get_graph_driver() as driver:
        with driver.session() as session:
            result = session.run("MATCH (t:Thread {id: $thread_id}) RETURN t", thread_id=thread_id)
            record = result.single()
            return dict(record["t"] if record else {}) if record else None

def delete_thread(thread_id):
    with get_graph_driver() as driver:
        with driver.session() as session:
            session.run(
                "MATCH (t:Thread {id: $id}) DELETE t",
                id=thread_id
            )

# Entry CRUD (Graph)
def create_entry(thread_id, timestamp, properties):
    with get_graph_driver() as driver:
        with driver.session() as session:
            result = session.run(
                """
                MATCH (t:Thread {id: $thread_id})
                CREATE (e:Entry {id: randomUUID(), timestamp: $timestamp, properties: $properties})
                CREATE (t)-[:HAS_ENTRY]->(e)
                RETURN e.id AS id
                """,
                thread_id=thread_id, timestamp=timestamp.isoformat(), properties=properties
            )
            return result.single()["id"]

def get_entries_by_thread(thread_id):
    with get_graph_driver() as driver:
        with driver.session() as session:
            result = session.run(
                """
                MATCH (t:Thread {id: $thread_id})-[:HAS_ENTRY]->(e:Entry)
                RETURN e
                """,
                thread_id=thread_id
            )
            return [record["e"] for record in result]

def get_entry_by_id(entry_id):
    with get_graph_driver() as driver:
        with driver.session() as session:
            result = session.run(
                "MATCH (e:Entry {id: $id}) RETURN e",
                id=entry_id
            )
            return result.single()["e"] if result.single() else None

def delete_entry(entry_id):
    with get_graph_driver() as driver:
        with driver.session() as session:
            session.run(
                "MATCH (e:Entry {id: $id}) DELETE e",
                id=entry_id
            )

# Snapshot CRUD (Graph)
def create_snapshot(thread_id, created_at, payload):
    with get_graph_driver() as driver:
        with driver.session() as session:
            result = session.run(
                """
                MATCH (t:Thread {id: $thread_id})
                CREATE (s:Snapshot {id: randomUUID(), created_at: $created_at, payload: $payload})
                CREATE (t)-[:HAS_SNAPSHOT]->(s)
                RETURN s.id AS id
                """,
                thread_id=thread_id, created_at=created_at.isoformat(), payload=payload
            )
            return result.single()["id"]

def get_snapshots_by_thread(thread_id):
    with get_graph_driver() as driver:
        with driver.session() as session:
            result = session.run(
                """
                MATCH (t:Thread {id: $thread_id})-[:HAS_SNAPSHOT]->(s:Snapshot)
                RETURN s
                """,
                thread_id=thread_id
            )
            return [record["s"] for record in result]

# Tag CRUD (Graph)
def create_tag(name):
    with get_graph_driver() as driver:
        with driver.session() as session:
            result = session.run(
                """
                CREATE (tag:Tag {id: randomUUID(), name: $name})
                RETURN tag.id AS id
                """,
                name=name
            )
            return result.single()["id"]

def get_tag_by_name(name):
    with get_graph_driver() as driver:
        with driver.session() as session:
            result = session.run(
                "MATCH (tag:Tag {name: $name}) RETURN tag",
                name=name
            )
            record = result.single()
            return record["tag"] if record else None

# Template CRUD (Graph)
def create_template(name, structure):
    with get_graph_driver() as driver:
        with driver.session() as session:
            result = session.run(
                """
                CREATE (tpl:Template {id: randomUUID(), name: $name, structure: $structure})
                RETURN tpl.id AS id
                """,
                name=name, structure=structure
            )
            return result.single()["id"]

def get_template_by_name(name):
    with get_graph_driver() as driver:
        with driver.session() as session:
            result = session.run(
                "MATCH (tpl:Template {name: $name}) RETURN tpl",
                name=name
            )
            record = result.single()
            return record["tpl"] if record else None

# --- Relationship/Edge Creation Functions ---

def link_entry_to_entry(source_entry_id, target_entry_id):
    """Create a LINKS_TO edge from one Entry to another."""
    with get_graph_driver() as driver:
        with driver.session() as session:
            session.run(
                """
                MATCH (src:Entry {id: $source_entry_id}), (tgt:Entry {id: $target_entry_id})
                MERGE (src)-[:LINKS_TO]->(tgt)
                """,
                source_entry_id=source_entry_id, target_entry_id=target_entry_id
            )

def tag_thread(thread_id, tag_name):
    """Tag a Thread with a Tag node (creates TAGGED_AS edge)."""
    with get_graph_driver() as driver:
        with driver.session() as session:
            session.run(
                """
                MATCH (t:Thread {id: $thread_id})
                MERGE (tag:Tag {name: $tag_name})
                MERGE (t)-[:TAGGED_AS]->(tag)
                """,
                thread_id=thread_id, tag_name=tag_name
            )

def tag_entry(entry_id, tag_name):
    """Tag an Entry with a Tag node (creates TAGGED_AS edge)."""
    with get_graph_driver() as driver:
        with driver.session() as session:
            session.run(
                """
                MATCH (e:Entry {id: $entry_id})
                MERGE (tag:Tag {name: $tag_name})
                MERGE (e)-[:TAGGED_AS]->(tag)
                """,
                entry_id=entry_id, tag_name=tag_name
            )

def assign_template_to_thread(thread_id, template_id):
    """Assign a Template to a Thread (USES_TEMPLATE edge)."""
    with get_graph_driver() as driver:
        with driver.session() as session:
            session.run(
                """
                MATCH (t:Thread {id: $thread_id}), (tpl:Template {id: $template_id})
                MERGE (t)-[:USES_TEMPLATE]->(tpl)
                """,
                thread_id=thread_id, template_id=template_id
            )

# --- Traversal/Query Functions ---

def get_linked_entries(entry_id):
    """Return all entries directly linked from the given entry."""
    with get_graph_driver() as driver:
        with driver.session() as session:
            result = session.run(
                """
                MATCH (e:Entry {id: $entry_id})-[:LINKS_TO]->(linked:Entry)
                RETURN linked
                """,
                entry_id=entry_id
            )
            return [record["linked"] for record in result]

def get_tags_for_thread(thread_id):
    """Return all tags for a thread."""
    with get_graph_driver() as driver:
        with driver.session() as session:
            result = session.run(
                """
                MATCH (t:Thread {id: $thread_id})-[:TAGGED_AS]->(tag:Tag)
                RETURN tag
                """,
                thread_id=thread_id
            )
            return [record["tag"] for record in result]

def get_tags_for_entry(entry_id):
    """Return all tags for an entry."""
    with get_graph_driver() as driver:
        with driver.session() as session:
            result = session.run(
                """
                MATCH (e:Entry {id: $entry_id})-[:TAGGED_AS]->(tag:Tag)
                RETURN tag
                """,
                entry_id=entry_id
            )
            return [record["tag"] for record in result]

def get_template_for_thread(thread_id):
    """Return the template assigned to a thread, if any."""
    with get_graph_driver() as driver:
        with driver.session() as session:
            result = session.run(
                """
                MATCH (t:Thread {id: $thread_id})-[:USES_TEMPLATE]->(tpl:Template)
                RETURN tpl
                """,
                thread_id=thread_id
            )
            record = result.single()
            return record["tpl"] if record else None

if __name__ == '__main__':
    # The database is initialized with the first capsule for testing purposes.
    create_capsule("Initial Capsule", "This is an initial capsule for testing.", datetime.now())
