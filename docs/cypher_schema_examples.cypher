# Cypher Schema Setup for Recall (Neo4j)
# Run these in Neo4j Browser or cypher-shell as needed.

// Ensure unique IDs for all major node types
CREATE CONSTRAINT capsule_id_unique IF NOT EXISTS FOR (c:Capsule) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT thread_id_unique IF NOT EXISTS FOR (t:Thread) REQUIRE t.id IS UNIQUE;
CREATE CONSTRAINT entry_id_unique IF NOT EXISTS FOR (e:Entry) REQUIRE e.id IS UNIQUE;
CREATE CONSTRAINT snapshot_id_unique IF NOT EXISTS FOR (s:Snapshot) REQUIRE s.id IS UNIQUE;
CREATE CONSTRAINT tag_id_unique IF NOT EXISTS FOR (tag:Tag) REQUIRE tag.id IS UNIQUE;
CREATE CONSTRAINT template_id_unique IF NOT EXISTS FOR (tpl:Template) REQUIRE tpl.id IS UNIQUE;

// Example: Create a Capsule, Thread, and Entry and link them
CREATE (c:Capsule {id: 'abc', name: 'Test Capsule', description: '...', created_at: '2025-06-13T00:00:00Z'})
CREATE (t:Thread {id: 'def', name: 'Thread1', created_at: '2025-06-13T00:00:00Z'})
CREATE (e:Entry {id: 'ghi', timestamp: '2025-06-13T00:00:00Z', properties: {foo: 'bar'}})
CREATE (c)-[:HAS_THREAD]->(t)
CREATE (t)-[:HAS_ENTRY]->(e);

// Example: Tag a Thread
MERGE (tag:Tag {name: 'important'})
MATCH (t:Thread {id: 'def'})
MERGE (t)-[:TAGGED_AS]->(tag);

// Example: Link Entries
MATCH (e1:Entry {id: 'ghi'}), (e2:Entry {id: 'xyz'})
MERGE (e1)-[:LINKS_TO]->(e2);

// Example: Assign Template to Thread
MATCH (t:Thread {id: 'def'}), (tpl:Template {id: 'tpl1'})
MERGE (t)-[:USES_TEMPLATE]->(tpl);
