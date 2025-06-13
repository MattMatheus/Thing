# MODEL.md

## Project Overview

**Thing** is a Flask-based web application for tracking arbitrary lists of things. Users can create custom list types, each with a set of properties (fields) of variable length and type (string, number, boolean). The app uses SQLite for data storage and is styled for dark mode using Bootstrap Dark. The UI is single-page-app-like, with dynamic list viewing and management.

## Data Model

### List Types
- Each list type is defined by the user and stored in the `thing_lists` table.
- Each list type has:
  - `id` (integer, primary key)
  - `name` (string, unique)
- When a new list type is created, a new table is created in the database with the sanitized name of the list.
- Each property of a list type has:
  - `name` (string)
  - `type` (string: 'string', 'number', 'boolean')
  - `default` (optional, type-dependent)
- Property types are mapped to SQLite types:
  - `string` → `TEXT`
  - `number` → `REAL`
  - `boolean` → `INTEGER` (0/1)

### List Objects
- Each object in a list type is a row in the corresponding table.
- Each object has an `id` (primary key) and columns for each property.

## Features

- **Landing Page**: Shows all list types with a count of objects in each. Filter and create controls are inline and styled for dark mode.
- **Create List Type**: Users can define a new list type with any number of properties, each with a name, type, and default value. Property type is selected from a dropdown.
- **View List**: Clicking a list shows its objects and allows adding or deleting objects. The list can be deleted (with confirmation by typing the list name).
- **SPA-like Navigation**: List views are loaded dynamically below the main controls. The main list view is hidden when a list is open.
- **Dark Mode**: All views use Bootstrap Dark and a custom `dark.css` for a consistent dark appearance.

## File Structure

- `thing.py` — Main Flask app, routes, and logic
- `db.py` — Database connection and initialization
- `requirements.txt` — Python dependencies
- `thing.db` — SQLite database
- `static/dark.css` — Central dark mode CSS
- `templates/` — Jinja2 HTML templates:
  - `index.html` — Main/landing page
  - `create_list.html` — Create new list type
  - `view_list.html` — View/manage a list type

## Future Agent Instructions
- Update this file whenever the data model or major features change.
- If adding new property types, update the type mapping in both the backend and the UI dropdown.
- If adding new features (e.g., user accounts, sharing, etc.), document the new tables, fields, and flows here.
- Keep all UI elements styled for dark mode using Bootstrap classes and `dark.css`.