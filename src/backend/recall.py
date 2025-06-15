from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from db import (
    create_capsule, get_all_capsules, get_capsule_by_id, delete_capsule,
    create_entry, get_entries_by_capsule, get_entry_by_id, delete_entry,
    create_tag, get_tag_by_name,
    link_entry_to_entry, get_linked_entries, get_linked_entries_recursive,
    search_entries_by_text, filter_entries_by_tag
)
import json
from datetime import datetime, UTC
import os
from flasgger import Swagger
from controllers.capsule_controller import capsule_bp
from controllers.entry_controller import entry_bp

# Set the template folder to src/frontend/templates (robust, with debug print)
TEMPLATE_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '../frontend/templates'))
STATIC_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '../frontend/static'))
print(f"[Recall] Using template folder: {TEMPLATE_DIR}")
print(f"[Recall] Using static folder: {STATIC_DIR}")
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key = 'recall-secret-key'
swagger = Swagger(app)

# Register blueprints
app.register_blueprint(capsule_bp)
app.register_blueprint(entry_bp)

@app.route('/create-capsule', methods=['GET', 'POST'])
def create_capsule_route():
    if request.method == 'POST':
        capsule_name = request.form['capsule_name']
        capsule_desc = request.form.get('capsule_description', '')
        fields_json = request.form.get('fields_json', '[]')
        fields = json.loads(fields_json)
        capsule_id = create_capsule(capsule_name, capsule_desc, datetime.now(UTC), fields)
        flash('Capsule created successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('create_capsule.html')

@app.route('/', methods=['GET'])
def home():
    capsules = get_all_capsules()
    return render_template('index.html', capsules=capsules, app_name='Recall')

@app.route('/capsule/<capsule_id>', methods=['GET', 'POST'])
def view_capsule(capsule_id):
    capsule = get_capsule_by_id(capsule_id)
    if not capsule:
        flash('Capsule not found.', 'danger')
        return redirect(url_for('home'))
    fields = capsule.get('fields', [])
    if request.method == 'POST':
        if 'add_entry' in request.form:
            entry_data = {}
            for field in fields:
                val = request.form.get(field['name'])
                if field['type'] == 'int':
                    try:
                        val = int(val)
                    except Exception:
                        val = 0
                elif field['type'] == 'boolean':
                    val = val == 'on' or val == 'true' or val is True
                entry_data[field['name']] = val
            create_entry(capsule_id, datetime.now(UTC), json.dumps(entry_data))
            flash('Entry added.', 'success')
        elif 'delete_entry' in request.form:
            entry_id = request.form.get('delete_entry')
            if entry_id:
                try:
                    delete_entry(entry_id)
                    flash('Entry deleted.', 'success')
                except Exception as e:
                    flash(f'Error deleting entry: {e}', 'danger')
            else:
                flash('Invalid entry ID.', 'danger')
        elif 'delete_capsule' in request.form:
            delete_capsule(capsule_id)
            flash('Capsule deleted.', 'success')
            return redirect(url_for('home'))
    entries = get_entries_by_capsule(capsule_id)
    # Prepare entries for template: parse properties and avoid mutating Node objects
    parsed_entries = []
    for entry in entries:
        entry_dict = dict(entry) if not isinstance(entry, dict) else entry.copy()
        props = entry_dict.get('properties')
        if isinstance(props, str):
            try:
                entry_dict['properties'] = json.loads(props)
            except Exception:
                entry_dict['properties'] = {}
        elif props is None:
            entry_dict['properties'] = {}
        parsed_entries.append(entry_dict)
    return render_template('view_capsule.html', capsule=capsule, entries=parsed_entries, fields=fields, app_name='Recall')

@app.route('/apidocs')
def apidocs_redirect():
    """Redirect /apidocs to the Flasgger Swagger UI."""
    return redirect('/apidocs/')
