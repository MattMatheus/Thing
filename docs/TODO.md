📌 Recall Implementation Plan — Vibecoding Edition

This plan provides a clear, incremental task breakdown for a coding agent to evolve Recall from a flat SQLite structure to a graph-backed, feature-rich datastore supporting tagging, linking, powerful search, visualization, and templates.

Infrastructure for the graph database will be handled separately.

⸻

✅ 1️⃣ Initial Setup & Refactor

# Task 1.1 — Refactor Domain Model
- [x] Rename classes & files to: Capsule, Thread, Entry, Snapshot
- [x] Migrate existing SQLite schema to match hierarchy (now graph-based)
- [x] Remove old or redundant structures

# Task 1.2 — Abstract Data Access Layer
- [x] Create an interface or service layer to handle CRUD operations (Neo4j)
- [x] Encapsulate storage-specific logic (SQLite → GraphDB switch)

# Task 1.3 — Unit Tests
- [ ] Add tests for new models and CRUD endpoints

⸻

✅ 2️⃣ Graph Database Integration

# Task 2.1 — Define Canonical Graph Schema
- [x] Nodes: Capsule, Thread, Entry, Tag, Template
- [x] Edges: HAS_THREAD, HAS_ENTRY, LINKS_TO, TAGGED_AS, USES_TEMPLATE

# Task 2.2 — Implement Graph DB Client
- [x] Add connection config
- [x] Implement node and edge creation functions
- [x] Replace SQLite queries with graph traversal queries

# Task 2.3 — Migration Script
- [x] (Skipped; not needed)

⸻

✅ 3️⃣ Core CRUD API

# Task 3.1 — Capsule & Thread Endpoints
- [x] GET /capsules
- [x] POST /capsules
- [x] GET /capsules/{id}/threads
- [x] POST /capsules/{id}/threads

# Task 3.2 — Entry Endpoints
- [x] GET /threads/{id}/entries
- [x] POST /threads/{id}/entries

# Task 3.3 — Snapshot Endpoint
- [x] POST /threads/{id}/snapshot
- [x] GET /threads/{id}/snapshot

# Task 3.4 — Add Basic Validation
- [x] Ensure all new objects conform to schema (UUID string IDs, Neo4j integration, and Flask routes fixed)

⸻

✅ 4️⃣ Tagging System

# Task 4.1 — Tag Node & Edge
- [x] Implement Tag node model
- [x] Add TAGGED_AS edge logic

# Task 4.2 — Tag CRUD
- [x] POST /tags
- [x] POST /threads/{id}/tags
- [x] GET /threads?tag={tag}

# Task 4.3 — Tag-Based Query
- [x] Add graph query to filter Threads or Entries by Tags

⸻

✅ 5️⃣ Relationships & Linking

# Task 5.1 — Links Between Entries
- [x] Add LINKS_TO edge model
- [x] POST /entries/{id}/link with target Entry ID
- [x] GET /entries/{id}/links

# Task 5.2 — Query Linked Data
- [ ] Traverse and fetch linked Entries recursively if needed

⸻

✅ 6️⃣ Search & Filter

Task 6.1 — Full-Text or Property Search
	•	Implement text search on Entry properties
	•	Filter by Tags, date, or custom fields

Task 6.2 — Combined Search API
	•	GET /search?tag=X&text=Y&linked_to=Z

⸻

✅ 7️⃣ Visualization API

Task 7.1 — Graph Export Endpoints
	•	GET /threads/{id}/graph
	•	GET /capsules/{id}/graph
	•	Return minimal graph representation (nodes & edges)

Task 7.2 — Prepare for Frontend Graph Viewer
	•	Ensure API output is compatible with graph libraries (e.g., Cytoscape.js)

⸻

✅ 8️⃣ Templates & Automation

Task 8.1 — Template Node
	•	Define Template node with structure metadata

Task 8.2 — Template CRUD
	•	POST /templates
	•	GET /templates

Task 8.3 — Apply Templates
	•	Allow POST /threads with template_id
	•	Auto-create default Entries per Template structure

⸻

✅ 9️⃣ Cleanup & Polish

Task 9.1 — Code Review & Refactor
	•	Ensure consistency in naming, docstrings, and logs

Task 9.2 — Add Docs
	•	Document API routes, payloads, and example graph queries

Task 9.3 — Final Tests
	•	Verify all core flows: tagging, linking, searching, visual graph output, templates

⸻

🚀 Next

Once these tasks are implemented incrementally, Recall will support its evolved feature set on a graph database foundation, aligning perfectly with the intended flexibility and exploration vibe.