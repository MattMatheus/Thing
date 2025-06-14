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
            result = session.run(
                "MATCH (c:Capsule {id: $id}) RETURN c",
                id=capsule_id
            )
            return result.single()["c"] if result.single() else None

def delete_capsule(capsule_id):
    with get_graph_driver() as driver:
        with driver.session() as session:
            session.run(
                "MATCH (c:Capsule {id: $id}) DELETE c",
                id=capsule_id
            )

# Thread CRUD

def create_thread(capsule_id, name, tags, created_at):
    with get_graph_driver() as driver:
        with driver.session() as session:
            result = session.run(
                """
                MATCH (c:Capsule {id: $capsule_id})
                CREATE (t:Thread {id: randomUUID(), name: $name, tags: $tags, created_at: $created_at})
                MERGE (c)-[:CONTAINS]->(t)
                RETURN t.id AS id
                """,
                capsule_id=capsule_id, name=name, tags=tags, created_at=created_at.isoformat()
            )
            return result.single()["id"]

def get_threads_by_capsule(capsule_id):
    with get_graph_driver() as driver:
        with driver.session() as session:
            result = session.run(
                "MATCH (c:Capsule {id: $capsule_id})-[:CONTAINS]->(t:Thread) RETURN t",
                capsule_id=capsule_id
            )
            return [record["t"] for record in result]

def get_thread_by_id(thread_id):
    with get_graph_driver() as driver:
        with driver.session() as session:
            result = session.run(
                "MATCH (t:Thread {id: $id}) RETURN t",
                id=thread_id
            )
            return result.single()["t"] if result.single() else None

def delete_thread(thread_id):
    with get_graph_driver() as driver:
        with driver.session() as session:
            session.run(
                "MATCH (t:Thread {id: $id}) DELETE t",
                id=thread_id
            )

# Entry CRUD

def create_entry(thread_id, timestamp, properties_json):
    with get_graph_driver() as driver:
        with driver.session() as session:
            result = session.run(
                """
                MATCH (t:Thread {id: $thread_id})
                CREATE (e:Entry {id: randomUUID(), timestamp: $timestamp, properties: $properties_json})
                MERGE (t)-[:HAS_ENTRY]->(e)
                RETURN e.id AS id
                """,
                thread_id=thread_id, timestamp=timestamp.isoformat(), properties_json=properties_json
            )
            return result.single()["id"]

def get_entries_by_thread(thread_id):
    with get_graph_driver() as driver:
        with driver.session() as session:
            result = session.run(
                "MATCH (t:Thread {id: $thread_id})-[:HAS_ENTRY]->(e:Entry) RETURN e",
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

if __name__ == '__main__':
    # The database is initialized with the first capsule for testing purposes.
    create_capsule("Initial Capsule", "This is an initial capsule for testing.", datetime.now())
