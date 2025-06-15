from flask import Blueprint, request, jsonify
from db import (
    create_capsule, get_all_capsules, get_capsule_by_id, delete_capsule,
    create_entry, get_entries_by_capsule, get_entry_by_id, delete_entry
)
from datetime import datetime, UTC
import json

capsule_bp = Blueprint('capsule_bp', __name__)

@capsule_bp.route('/api/capsules', methods=['GET'])
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

@capsule_bp.route('/api/capsule/<capsule_id>', methods=['GET'])
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

@capsule_bp.route('/api/capsule/<capsule_id>/add_entry', methods=['POST'])
def api_add_entry(capsule_id):
    capsule = get_capsule_by_id(capsule_id)
    if not capsule:
        return jsonify({'error': 'Capsule not found'}), 404
    properties = request.json.get('properties', '{}')
    create_entry(capsule_id, datetime.now(UTC), json.dumps(properties))
    return jsonify({'success': True})

@capsule_bp.route('/api/capsule/<capsule_id>/delete_entry', methods=['POST'])
def api_delete_entry(capsule_id):
    """
    Delete an entry from a capsule
    ---
    tags:
      - Entries
    parameters:
      - name: capsule_id
        in: path
        type: string
        required: true
        description: ID of the capsule
      - name: id
        in: body
        required: true
        schema:
          type: object
          properties:
            id:
              type: string
              description: ID of the entry to delete
    responses:
      200:
        description: Entry deleted successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
      404:
        description: Capsule not found
        schema:
          type: object
          properties:
            error:
              type: string
    """
    entry_id = request.json.get('id')
    capsule = get_capsule_by_id(capsule_id)
    if not capsule:
        return jsonify({'error': 'Capsule not found'}), 404
    delete_entry(entry_id)
    return jsonify({'success': True})

@capsule_bp.route('/api/capsule/<capsule_id>/delete', methods=['POST'])
def api_delete_capsule(capsule_id):
    """
    Delete a capsule
    ---
    tags:
      - Capsules
    parameters:
      - name: capsule_id
        in: path
        type: string
        required: true
        description: ID of the capsule to delete
    responses:
      200:
        description: Capsule deleted successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
      404:
        description: Capsule not found
        schema:
          type: object
          properties:
            error:
              type: string
    """
    capsule = get_capsule_by_id(capsule_id)
    if not capsule:
        return jsonify({'error': 'Capsule not found'}), 404
    delete_capsule(capsule_id)
    return jsonify({'success': True})
