# MODEL.md

## Project Overview

**Recall** is a Flask-based web application for tracking arbitrary capsules of information. Users can create custom capsule types, each with a set of properties (fields) of variable length and type (string, number, boolean). The app uses Neo4j for data storage and is styled for dark mode using Bootstrap Dark. The UI is single-page-app-like, with dynamic capsule viewing and management.

## Data Model (Graph-Based, Neo4j)

### Nodes
- **Capsule**: Represents a collection of entries.
- **Entry**: Belongs to a Capsule, can link to other Entries.
- **Snapshot**: Captures the state of an Entry at a point in time.
- **Tag**: Used for categorization and filtering. Tags are unique by name and can be attached to Entries via the TAGGED_AS edge. Tags have: `id`, `name`.
- **Template**: Defines structure metadata for Entries.

### Relationships (Edges)
- `HAS_ENTRY`: Capsule → Entry
- `LINKS_TO`: Entry → Entry. Entries can be linked to other entries using the `link_entry_to_entry` backend function and the `/api/entries/<entry_id>/link` API endpoint. Linked entries can be retrieved with `/api/entries/<entry_id>/links`.
- `TAGGED_AS`: Entry → Tag. Used to associate tags with entries. Created via the tag_entry backend function and exposed via the API.
- `USES_TEMPLATE`: Entry → Template

### Example Node Properties
- Capsule: `id`, `name`, `description`, `created_at`
- Entry: `id`, `timestamp`, `properties`
- Snapshot: `id`, `created_at`, `payload`
- Tag: `id`, `name`
- Template: `id`, `name`, `structure`

## Backend Changes
- All data is now stored in Neo4j (see .env for connection config).
- All CRUD and query operations use the Neo4j Python driver.
- SQLite and related code have been removed.
- All core CRUD flows (Capsule, Entry, Snapshot) are now fully functional and integrated with Neo4j.
- All Flask routes and API endpoints use string (UUID) IDs for graph objects.
- Template folder is set to `src/frontend/templates` for all UI rendering.
- Known issues with ID types and retrieval have been resolved.
- Tag CRUD and tag-assignment endpoints:
  - `POST /api/tags` — Create a new tag (name required)
  - `POST /api/entry/<entry_id>/tags` — Tag an entry with a tag (creates TAGGED_AS edge)
  - `GET /api/entries?tag={tag}` — List entries tagged with a given tag
- Entry linking endpoints:
  - `POST /api/entries/<entry_id>/link` — Link an entry to another entry (creates LINKS_TO edge)
  - `GET /api/entries/<entry_id>/links` — Get all entries linked from a given entry

## Features

- **Landing Page**: Shows all capsule types with a count of entries in each. Filter and create controls are inline and styled for dark mode.
- **Create Capsule Type**: Users can define a new capsule type with any number of properties, each with a name, type, and default value. Property type is selected from a dropdown.
- **View Capsule**: Clicking a capsule shows its entries and allows adding or deleting entries. The capsule can be deleted (with confirmation by typing the capsule name).
- **SPA-like Navigation**: Capsule views are loaded dynamically below the main controls. The main capsule view is hidden when a capsule is open.
- **Dark Mode**: All views use Bootstrap Dark and a custom `dark.css` for a consistent dark appearance.

## File Structure

- `recall.py` — Main Flask app, routes, and logic
- `db.py` — Database connection and initialization
- `requirements.txt` — Python dependencies
- `docs/cypher_schema_examples.cypher` — Example Cypher commands for Neo4j schema setup and manual data manipulation
- `thing.db` — SQLite database (legacy, not used)
- `static/dark.css` — Central dark mode CSS
- `templates/` — Jinja2 HTML templates:
  - `index.html` — Main/landing page
  - `create_capsule.html` — Create new capsule type
  - `view_capsule.html` — View/manage a capsule type

## Future Agent Instructions
- Update this file whenever the data model or major features change.
- If adding new property types, update the type mapping in both the backend and the UI dropdown.
- If adding new features (e.g., user accounts, sharing, etc.), document the new tables, fields, and flows here.
- Keep all UI elements styled for dark mode using Bootstrap classes and `dark.css`.