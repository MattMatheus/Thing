# MODEL.md

## Project Overview

**Recall** is a Flask-based web application for tracking arbitrary capsules of information. Users can create custom capsule types, each with a set of properties (fields) of variable length and type (string, number, boolean). The app uses SQLite for data storage and is styled for dark mode using Bootstrap Dark. The UI is single-page-app-like, with dynamic capsule viewing and management.

## Data Model

### Capsule Types
- Each capsule type is defined by the user and stored in the `thing_lists` table.
- Each capsule type has:
  - `id` (integer, primary key)
  - `name` (string, unique)
- When a new capsule type is created, a new table is created in the database with the sanitized name of the capsule.
- Each property of a capsule type has:
  - `name` (string)
  - `type` (string: 'string', 'number', 'boolean')
  - `default` (optional, type-dependent)
- Property types are mapped to SQLite types:
  - `string` → `TEXT`
  - `number` → `REAL`
  - `boolean` → `INTEGER` (0/1)

### Capsule Entries
- Each entry in a capsule type is a row in the corresponding table.
- Each entry has an `id` (primary key) and columns for each property.

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
- `thing.db` — SQLite database
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