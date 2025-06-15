import os
import pytest
import json
from datetime import datetime, UTC
from src.backend import db

# Ensure test Neo4j instance is running and .env is configured

def test_create_and_get_capsule():
    name = "Test Capsule"
    description = "A test capsule."
    created_at = datetime.now(UTC)
    capsule_id = db.create_capsule(name, description, created_at)
    assert capsule_id is not None
    capsules = db.get_all_capsules()
    assert any(c["id"] == capsule_id for c in capsules)

def test_create_and_get_entry():
    capsule_id = db.create_capsule("Entry Capsule", "desc", datetime.now(UTC))
    entry_id = db.create_entry(capsule_id, datetime.now(UTC), json.dumps({"foo": "bar"}))
    assert entry_id is not None
    entries = db.get_entries_by_capsule(capsule_id)
    assert any(e["id"] == entry_id for e in entries)

def test_create_and_get_snapshot():
    capsule_id = db.create_capsule("Snap Capsule", "desc", datetime.now(UTC))
    entry_id = db.create_entry(capsule_id, datetime.now(UTC), json.dumps({"foo": "bar"}))
    snap_id = db.create_snapshot(entry_id, datetime.now(UTC), json.dumps({"snap": 1}))
    assert snap_id is not None
    snaps = db.get_snapshots_by_entry(entry_id)
    assert any(s["id"] == snap_id for s in snaps)

def test_create_and_get_tag():
    tag_id = db.create_tag("testtag")
    assert tag_id is not None
    tag = db.get_tag_by_name("testtag")
    assert tag is not None
    assert tag["name"] == "testtag"

def test_create_and_get_template():
    tpl_id = db.create_template("tpl", json.dumps({"fields": ["a"]}))
    assert tpl_id is not None
    tpl = db.get_template_by_name("tpl")
    assert tpl is not None
    assert tpl["name"] == "tpl"

@pytest.fixture(autouse=True)
def cleanup_db():
    # Clean up all test capsules and related entries after each test
    from src.backend import db
    yield
    # Remove all capsules with names starting with 'pytest_capsule' or 'Test Capsule' or similar
    with db.get_graph_driver() as driver:
        with driver.session() as session:
            session.run("""
                MATCH (c:Capsule)
                WHERE c.name STARTS WITH 'pytest_capsule' OR c.name STARTS WITH 'Test Capsule' OR c.name CONTAINS 'Capsule'
                DETACH DELETE c
            """)
            # Also clean up test tags and templates
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
