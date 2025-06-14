# MODEL.md

## Project Overview

**Recall** is a Flask-based web application for tracking arbitrary capsules of information. Users can create custom capsule types, each with a set of properties (fields) of variable length and type (string, number, boolean). The app uses Neo4j for data storage and is styled for dark mode using Bootstrap Dark. The UI is single-page-app-like, with dynamic capsule viewing and management.

## Data Model (Graph-Based, Neo4j)

### Nodes
- **Capsule**: Represents a collection of threads.
- **Thread**: Belongs to a Capsule, contains Entries, can have Tags.
- **Entry**: Belongs to a Thread, can link to other Entries.
- **Snapshot**: Captures the state of a Thread at a point in time.
- **Tag**: Used for categorization and filtering.
- **Template**: Defines structure metadata for Threads/Entries.

### Relationships (Edges)
- `HAS_THREAD`: Capsule → Thread
- `HAS_ENTRY`: Thread → Entry
- `LINKS_TO`: Entry → Entry
- `TAGGED_AS`: Thread/Entry → Tag
- `USES_TEMPLATE`: Thread → Template

### Example Node Properties
- Capsule: `id`, `name`, `description`, `created_at`
- Thread: `id`, `name`, `created_at`, `tags`
- Entry: `id`, `timestamp`, `properties`
- Snapshot: `id`, `created_at`, `payload`
- Tag: `id`, `name`
- Template: `id`, `name`, `structure`

## Backend Changes
- All data is now stored in Neo4j (see .env for connection config).
- All CRUD and query operations use the Neo4j Python driver.
- SQLite and related code have been removed.
- All core CRUD flows (Capsule, Thread, Entry, Snapshot) are now fully functional and integrated with Neo4j.
- All Flask routes and API endpoints use string (UUID) IDs for graph objects.
- Template folder is set to `src/frontend/templates` for all UI rendering.
- Known issues with ID types and retrieval have been resolved.

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