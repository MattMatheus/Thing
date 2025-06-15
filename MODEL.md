# Recall Data Model & Features (2025)

## Core Node Types
- **Capsule**: Top-level container for threads and entries.
- **Thread**: (If used) Logical grouping of entries within a capsule.
- **Entry**: Main data node, supports arbitrary properties.
- **Snapshot**: Versioned state of an entry.
- **Tag**: Label node for categorization.
- **Template**: Defines structure/fields for threads or entries.

## Relationships (Edges)
- `HAS_THREAD`: Capsule → Thread
- `HAS_ENTRY`: Capsule/Thread → Entry
- `LINKS_TO`: Entry → Entry (arbitrary links)
- `TAGGED_AS`: Entry/Thread → Tag
- `USES_TEMPLATE`: Thread/Entry → Template

## API & Features
- **CRUD for Capsules, Threads, Entries, Snapshots, Tags, Templates**
- **Linking**: Entries can link to other entries (`LINKS_TO`)
- **Recursive Linked Data**: Traverse and fetch linked entries recursively via `/entries/{id}/links_recursive`
- **Search**: Full-text/property search, filter by tag/date/fields
- **Combined Search**: `/search?tag=X&text=Y&linked_to=Z`
- **Visualization**: Export graph structure for capsules/threads (Cytoscape.js compatible)
- **Templates**: Define and apply templates to threads/entries

## Testing
- **Pytest-based suite** for all CRUD endpoints and models
- **Database cleanup** after each test (autouse fixture)
- **Test coverage** includes: capsule, entry, snapshot, tag, template creation and retrieval, linking, and API flows

## Implementation Notes
- **Neo4j** is the backing store (see `db.py`)
- **Flask** provides the API layer
- **All properties** for entries/templates are stored as JSON strings for flexibility
- **UUIDs** are used for all node IDs
- **Validation**: All new objects are validated for schema and type
- Capsule and Entry API endpoints have been refactored into Flask blueprints:
  - `src/backend/controllers/capsule_controller.py` for capsule-related API routes
  - `src/backend/controllers/entry_controller.py` for entry-related API routes
- Blueprints are registered in `src/backend/recall.py`.
- All API logic is now organized by resource, improving maintainability and scalability.
- No changes to the data model or API contract.

---

This model supports flexible, graph-based data exploration, tagging, linking, and visualization, with robust automated tests and a clean, modern API.