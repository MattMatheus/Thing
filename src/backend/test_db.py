import os
import pytest
from datetime import datetime
from src.backend import db

# Ensure test Neo4j instance is running and .env is configured

def test_create_and_get_capsule():
    name = "Test Capsule"
    description = "A test capsule."
    created_at = datetime.utcnow()
    capsule_id = db.create_capsule(name, description, created_at)
    assert capsule_id is not None
    capsules = db.get_all_capsules()
    assert any(c["id"] == capsule_id for c in capsules)

def test_create_and_get_entry():
    capsule_id = db.create_capsule("Entry Capsule", "desc", datetime.utcnow())
    entry_id = db.create_entry(capsule_id, datetime.utcnow(), {"foo": "bar"})
    assert entry_id is not None
    entries = db.get_entries_by_capsule(capsule_id)
    assert any(e["id"] == entry_id for e in entries)

def test_create_and_get_snapshot():
    capsule_id = db.create_capsule("Snap Capsule", "desc", datetime.utcnow())
    entry_id = db.create_entry(capsule_id, datetime.utcnow(), {"foo": "bar"})
    snap_id = db.create_snapshot(entry_id, datetime.utcnow(), {"snap": 1})
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
    tpl_id = db.create_template("tpl", {"fields": ["a"]})
    assert tpl_id is not None
    tpl = db.get_template_by_name("tpl")
    assert tpl is not None
    assert tpl["name"] == "tpl"
