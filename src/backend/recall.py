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

# Set the template folder to src/frontend/templates (robust, with debug print)
TEMPLATE_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '../frontend/templates'))
print(f"[Recall] Using template folder: {TEMPLATE_DIR}")
app = Flask(__name__, template_folder=TEMPLATE_DIR)
app.secret_key = 'recall-secret-key'
swagger = Swagger(app)

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

# --- API Endpoints ---
@app.route('/api/capsules', methods=['GET'])
def api_get_all_capsules():
    """
    Get all capsules
    ---
    tags:
      - Capsules
    responses:
      200:
        description: List of all capsules
        schema:
          type: object
          properties:
            capsules:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                  name:
                    type: string
    """
    capsules = get_all_capsules()
    result = [
        {'id': row['id'], 'name': row['name']} for row in capsules
    ]
    return jsonify({'capsules': result})

@app.route('/api/capsule/<capsule_id>', methods=['GET'])
def api_get_capsule(capsule_id):
    capsule = get_capsule_by_id(capsule_id)
    if not capsule:
        return jsonify({'error': 'Capsule not found'}), 404
    entries = get_entries_by_capsule(capsule_id)
    return jsonify({
        'capsule_id': capsule_id,
        'capsule_name': capsule['name'],
        'description': capsule['description'],
        'entries': [dict(entry) for entry in entries]
    })

@app.route('/api/capsule/<capsule_id>/add_entry', methods=['POST'])
def api_add_entry(capsule_id):
    capsule = get_capsule_by_id(capsule_id)
    if not capsule:
        return jsonify({'error': 'Capsule not found'}), 404
    properties = request.json.get('properties', '{}')
    create_entry(capsule_id, datetime.now(UTC), json.dumps(properties))
    return jsonify({'success': True})

@app.route('/api/capsule/<capsule_id>/delete_entry', methods=['POST'])
def api_delete_entry(capsule_id):
    entry_id = request.json.get('id')
    capsule = get_capsule_by_id(capsule_id)
    if not capsule:
        return jsonify({'error': 'Capsule not found'}), 404
    delete_entry(entry_id)
    return jsonify({'success': True})

@app.route('/api/capsule/<capsule_id>/delete', methods=['POST'])
def api_delete_capsule(capsule_id):
    capsule = get_capsule_by_id(capsule_id)
    if not capsule:
        return jsonify({'error': 'Capsule not found'}), 404
    delete_capsule(capsule_id)
    return jsonify({'success': True})

@app.route('/api/entries/<entry_id>/link', methods=['POST'])
def api_link_entry(entry_id):
    data = request.get_json() or {}
    target_id = data.get('target_id')
    if not target_id:
        return jsonify({'error': 'Target entry ID required'}), 400
    link_entry_to_entry(entry_id, target_id)
    return jsonify({'success': True})

@app.route('/api/entries/<entry_id>/links', methods=['GET'])
def api_get_entry_links(entry_id):
    linked = get_linked_entries(entry_id)
    return jsonify({'linked_entries': [dict(e) for e in linked]})

@app.route('/api/entries/<entry_id>/links_recursive', methods=['GET'])
def api_get_entry_links_recursive(entry_id):
    linked = get_linked_entries_recursive(entry_id)
    # Remove duplicates by id
    seen = set()
    unique = []
    for e in linked:
        eid = e.get('id')
        if eid and eid not in seen:
            seen.add(eid)
            unique.append(dict(e))
    return jsonify({'linked_entries_recursive': unique})

@app.route('/api/entries/search', methods=['GET'])
def api_search_entries():
    text = request.args.get('text')
    tag = request.args.get('tag')
    results = set()
    if text:
        for e in search_entries_by_text(text):
            results.add(e['id'])
    if tag:
        for e in filter_entries_by_tag(tag):
            results.add(e['id'])
    # Fetch full entry objects for all result IDs
    entries = [dict(get_entry_by_id(eid)) for eid in results if get_entry_by_id(eid)]
    return jsonify({'entries': entries})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
