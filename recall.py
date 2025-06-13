from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from db import (
    init_db, create_capsule, get_all_capsules, get_capsule_by_id, delete_capsule,
    create_thread, get_threads_by_capsule, get_thread_by_id, delete_thread,
    create_entry, get_entries_by_thread, get_entry_by_id, delete_entry
)
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'recall-secret-key'

init_db()

@app.route('/create-capsule', methods=['GET', 'POST'])
def create_capsule_route():
    if request.method == 'POST':
        capsule_name = request.form['capsule_name']
        capsule_desc = request.form.get('capsule_description', '')
        capsule_id = create_capsule(capsule_name, capsule_desc, datetime.utcnow().isoformat())
        flash('Capsule created successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('create_capsule.html')

@app.route('/', methods=['GET'])
def home():
    capsules = get_all_capsules()
    return render_template('index.html', capsules=capsules, app_name='Recall')

@app.route('/capsule/<int:capsule_id>', methods=['GET', 'POST'])
def view_capsule(capsule_id):
    capsule = get_capsule_by_id(capsule_id)
    if not capsule:
        flash('Capsule not found.', 'danger')
        return redirect(url_for('home'))
    if request.method == 'POST':
        if 'add_thread' in request.form:
            thread_name = request.form['thread_name']
            tags = request.form.get('tags', '')
            create_thread(capsule_id, thread_name, tags, datetime.utcnow().isoformat())
            flash('Thread added.', 'success')
        elif 'delete_thread' in request.form:
            thread_id = request.form.get('delete_thread')
            delete_thread(thread_id)
            flash('Thread deleted.', 'success')
        elif 'delete_capsule' in request.form:
            delete_capsule(capsule_id)
            flash('Capsule deleted.', 'success')
            return redirect(url_for('home'))
    threads = get_threads_by_capsule(capsule_id)
    return render_template('view_capsule.html', capsule=capsule, threads=threads, app_name='Recall')

@app.route('/thread/<int:thread_id>', methods=['GET', 'POST'])
def view_thread(thread_id):
    thread = get_thread_by_id(thread_id)
    if not thread:
        flash('Thread not found.', 'danger')
        return redirect(url_for('home'))
    capsule = get_capsule_by_id(thread['capsule_id'])
    if request.method == 'POST':
        if 'add_entry' in request.form:
            properties = request.form.get('properties', '{}')
            # Accept properties as JSON string for now
            create_entry(thread_id, datetime.utcnow().isoformat(), properties)
            flash('Entry added.', 'success')
        elif 'delete_entry' in request.form:
            entry_id = request.form.get('delete_entry')
            delete_entry(entry_id)
            flash('Entry deleted.', 'success')
    entries = get_entries_by_thread(thread_id)
    return render_template('view_thread.html', thread=thread, capsule=capsule, entries=entries, app_name='Recall')

# --- API Endpoints ---
@app.route('/api/capsules', methods=['GET'])
def api_get_all_capsules():
    capsules = get_all_capsules()
    result = [
        {'id': row['id'], 'name': row['name']} for row in capsules
    ]
    return jsonify({'capsules': result})

@app.route('/api/capsule/<int:capsule_id>', methods=['GET'])
def api_get_capsule(capsule_id):
    capsule = get_capsule_by_id(capsule_id)
    if not capsule:
        return jsonify({'error': 'Capsule not found'}), 404
    threads = get_threads_by_capsule(capsule_id)
    return jsonify({
        'capsule_id': capsule_id,
        'capsule_name': capsule['name'],
        'description': capsule['description'],
        'threads': [dict(thread) for thread in threads]
    })

@app.route('/api/thread/<int:thread_id>', methods=['GET'])
def api_get_thread(thread_id):
    thread = get_thread_by_id(thread_id)
    if not thread:
        return jsonify({'error': 'Thread not found'}), 404
    entries = get_entries_by_thread(thread_id)
    return jsonify({
        'thread_id': thread_id,
        'thread_name': thread['name'],
        'tags': thread['tags'],
        'entries': [dict(entry) for entry in entries]
    })

@app.route('/api/thread/<int:thread_id>/add_entry', methods=['POST'])
def api_add_entry(thread_id):
    thread = get_thread_by_id(thread_id)
    if not thread:
        return jsonify({'error': 'Thread not found'}), 404
    properties = request.json.get('properties', '{}')
    create_entry(thread_id, datetime.utcnow().isoformat(), json.dumps(properties))
    return jsonify({'success': True})

@app.route('/api/thread/<int:thread_id>/delete_entry', methods=['POST'])
def api_delete_entry(thread_id):
    entry_id = request.json.get('id')
    thread = get_thread_by_id(thread_id)
    if not thread:
        return jsonify({'error': 'Thread not found'}), 404
    delete_entry(entry_id)
    return jsonify({'success': True})

@app.route('/api/capsule/<int:capsule_id>/delete', methods=['POST'])
def api_delete_capsule(capsule_id):
    capsule = get_capsule_by_id(capsule_id)
    if not capsule:
        return jsonify({'error': 'Capsule not found'}), 404
    delete_capsule(capsule_id)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
