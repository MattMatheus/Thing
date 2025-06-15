import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/backend')))

import pytest
from flask import json
from src.backend.recall import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def cleanup_db():
    # Clean up all test capsules and related entries after each test
    import importlib.util
    import sys
    import os
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/backend/db.py'))
    spec = importlib.util.spec_from_file_location('db', db_path)
    db = importlib.util.module_from_spec(spec)
    sys.modules['db'] = db
    spec.loader.exec_module(db)
    yield
    with db.get_graph_driver() as driver:
        with driver.session() as session:
            session.run("""
                MATCH (c:Capsule)
                WHERE c.name STARTS WITH 'pytest_capsule' OR c.name STARTS WITH 'Test Capsule' OR c.name CONTAINS 'Capsule'
                DETACH DELETE c
            """)
            session.run("""
                MATCH (t:Tag)
                WHERE t.name STARTS WITH 'testtag'
                DETACH DELETE t
            """)
            session.run("""
                MATCH (tpl:Template)
                WHERE tpl.name STARTS WITH 'tpl'
                DETACH DELETE tpl
            """)

def test_get_all_capsules(client):
    response = client.get('/api/capsules')
    assert response.status_code == 200
    data = response.get_json()
    assert 'capsules' in data

def test_create_and_get_capsule(client):
    import importlib.util
    import sys
    import os
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/backend/db.py'))
    spec = importlib.util.spec_from_file_location('db', db_path)
    db = importlib.util.module_from_spec(spec)
    sys.modules['db'] = db
    spec.loader.exec_module(db)
    import uuid
    from datetime import datetime, UTC
    capsule_name = f"pytest_capsule_{uuid.uuid4()}"
    capsule_desc = "pytest description"
    fields = [{"name": "field1", "type": "string"}]
    capsule_id = db.create_capsule(capsule_name, capsule_desc, datetime.now(UTC), fields)
    # Now get via API
    response = client.get(f"/api/capsule/{capsule_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["capsule_id"] == capsule_id
    assert data["capsule_name"] == capsule_name
    assert data["description"] == capsule_desc
    assert data["entries"] == []

def test_add_and_delete_entry(client):
    import importlib.util
    import sys
    import os
    from datetime import datetime, UTC
    import uuid
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/backend/db.py'))
    spec = importlib.util.spec_from_file_location('db', db_path)
    db = importlib.util.module_from_spec(spec)
    sys.modules['db'] = db
    spec.loader.exec_module(db)
    # Create a capsule
    capsule_name = f"pytest_capsule_{uuid.uuid4()}"
    capsule_desc = "pytest description"
    fields = [{"name": "field1", "type": "string"}]
    capsule_id = db.create_capsule(capsule_name, capsule_desc, datetime.now(UTC), fields)
    # Add entry via API
    entry_props = {"field1": "value1"}
    response = client.post(f"/api/capsule/{capsule_id}/add_entry", json={"properties": entry_props})
    assert response.status_code == 200
    # Get capsule and check entry exists
    response = client.get(f"/api/capsule/{capsule_id}")
    data = response.get_json()
    assert len(data["entries"]) == 1
    entry_id = data["entries"][0]["id"]
    # Delete entry via API
    response = client.post(f"/api/capsule/{capsule_id}/delete_entry", json={"id": entry_id})
    assert response.status_code == 200
    # Confirm entry deleted
    response = client.get(f"/api/capsule/{capsule_id}")
    data = response.get_json()
    assert data["entries"] == []

def test_delete_capsule(client):
    import importlib.util
    import sys
    import os
    from datetime import datetime, UTC
    import uuid
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/backend/db.py'))
    spec = importlib.util.spec_from_file_location('db', db_path)
    db = importlib.util.module_from_spec(spec)
    sys.modules['db'] = db
    spec.loader.exec_module(db)
    # Create a capsule
    capsule_name = f"pytest_capsule_{uuid.uuid4()}"
    capsule_desc = "pytest description"
    fields = [{"name": "field1", "type": "string"}]
    capsule_id = db.create_capsule(capsule_name, capsule_desc, datetime.now(UTC), fields)
    # Delete capsule via API
    response = client.post(f"/api/capsule/{capsule_id}/delete")
    assert response.status_code == 200
    # Confirm capsule deleted
    response = client.get(f"/api/capsule/{capsule_id}")
    assert response.status_code == 404
