from flask import Blueprint, request, jsonify
from db import (
    link_entry_to_entry, get_linked_entries, get_linked_entries_recursive,
    get_entry_by_id, search_entries_by_text, filter_entries_by_tag
)

entry_bp = Blueprint('entry_bp', __name__)

@entry_bp.route('/api/entries/<entry_id>/link', methods=['POST'])
def api_link_entry(entry_id):
    """
    Link one entry to another entry
    ---
    tags:
      - Entries
    parameters:
      - name: entry_id
        in: path
        type: string
        required: true
        description: ID of the source entry
      - name: target_id
        in: body
        required: true
        schema:
          type: object
          properties:
            target_id:
              type: string
              description: ID of the target entry to link to
    responses:
      200:
        description: Entries linked successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
      400:
        description: Target entry ID required
        schema:
          type: object
          properties:
            error:
              type: string
    """
    data = request.get_json() or {}
    target_id = data.get('target_id')
    if not target_id:
        return jsonify({'error': 'Target entry ID required'}), 400
    link_entry_to_entry(entry_id, target_id)
    return jsonify({'success': True})

@entry_bp.route('/api/entries/<entry_id>/links', methods=['GET'])
def api_get_entry_links(entry_id):
    linked = get_linked_entries(entry_id)
    return jsonify({'linked_entries': [dict(e) for e in linked]})

@entry_bp.route('/api/entries/<entry_id>/links_recursive', methods=['GET'])
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

@entry_bp.route('/api/entries/search', methods=['GET'])
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
