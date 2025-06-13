from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from db import (
    get_db_connection, init_db, create_list_type, get_all_lists, get_list_by_id,
    delete_list, get_list_columns, get_list_objects, add_object_to_list, delete_object_from_list, get_table_name
)

app = Flask(__name__)
app.secret_key = 'thing-secret-key'

init_db()

@app.route('/create-list', methods=['GET', 'POST'])
def create_list():
    if request.method == 'POST':
        list_name = request.form['list_name']
        # Collect properties
        properties = []
        idx = 0
        while True:
            prop_name = request.form.get(f'property_name_{idx}')
            prop_type = request.form.get(f'property_type_{idx}')
            prop_default = request.form.get(f'property_default_{idx}')
            if not prop_name:
                break
            properties.append((prop_name, prop_type, prop_default))
            idx += 1
        if not properties:
            flash('You must add at least one property.', 'danger')
            return render_template('create_list.html')
        # Sanitize table name
        table_name = get_table_name(list_name)
        if not table_name:
            flash('Invalid list name.', 'danger')
            return render_template('create_list.html')
        try:
            create_list_type(list_name, properties)
            flash('List type created successfully!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            flash(f'Error creating list: {e}', 'danger')
            return render_template('create_list.html')
    return render_template('create_list.html')

@app.route('/', methods=['GET'])
def home():
    filter_value = request.args.get('filter', '')
    thing_lists = get_all_lists(filter_value)
    return render_template('index.html', thing_lists=thing_lists, filter=filter_value)

@app.route('/list/<int:list_id>', methods=['GET', 'POST'])
def view_list(list_id):
    list_row = get_list_by_id(list_id)
    if not list_row:
        flash('List not found.', 'danger')
        return redirect(url_for('home'))
    list_name = list_row['name']
    # Handle add object
    if request.method == 'POST' and 'add_object' in request.form:
        data = {col: request.form.get(col, '') for col in get_list_columns(list_name)}
        add_object_to_list(list_name, data)
        flash('Object added.', 'success')
    # Handle delete object
    if request.method == 'POST' and 'delete_object' in request.form:
        obj_id = request.form.get('delete_object')
        delete_object_from_list(list_name, obj_id)
        flash('Object deleted.', 'success')
    # Handle delete list
    if request.method == 'POST' and 'delete_list' in request.form:
        delete_list(list_id, list_name)
        flash('List deleted.', 'success')
        return redirect(url_for('home'))
    columns = get_list_columns(list_name)
    objects = get_list_objects(list_name)
    return render_template('view_list.html', list_id=list_id, list_name=list_name, columns=columns, objects=objects)

@app.route('/api/list/<int:list_id>', methods=['GET'])
def api_get_list(list_id):
    list_row = get_list_by_id(list_id)
    if not list_row:
        return jsonify({'error': 'List not found'}), 404
    list_name = list_row['name']
    columns = get_list_columns(list_name)
    objects = get_list_objects(list_name)
    return jsonify({
        'list_id': list_id,
        'list_name': list_name,
        'columns': columns,
        'objects': [dict(obj) for obj in objects]
    })

@app.route('/api/list/<int:list_id>/add', methods=['POST'])
def api_add_object(list_id):
    list_row = get_list_by_id(list_id)
    if not list_row:
        return jsonify({'error': 'List not found'}), 404
    list_name = list_row['name']
    add_object_to_list(list_name, request.json)
    return jsonify({'success': True})

@app.route('/api/list/<int:list_id>/delete_object', methods=['POST'])
def api_delete_object(list_id):
    obj_id = request.json.get('id')
    list_row = get_list_by_id(list_id)
    if not list_row:
        return jsonify({'error': 'List not found'}), 404
    list_name = list_row['name']
    delete_object_from_list(list_name, obj_id)
    return jsonify({'success': True})

@app.route('/api/list/<int:list_id>/delete', methods=['POST'])
def api_delete_list(list_id):
    list_row = get_list_by_id(list_id)
    if not list_row:
        return jsonify({'error': 'List not found'}), 404
    list_name = list_row['name']
    delete_list(list_id, list_name)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
