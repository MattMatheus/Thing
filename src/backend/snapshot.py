from datetime import datetime
import uuid

class Snapshot:
    def __init__(self, id: str = None, thread_id: str = '', created_at: datetime = None, payload: dict = None):
        self.id = id or str(uuid.uuid4())
        self.thread_id = thread_id
        self.created_at = created_at or datetime.utcnow()
        self.payload = payload or {}
