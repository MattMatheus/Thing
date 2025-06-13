from datetime import datetime
import uuid

class Entry:
    def __init__(self, id: str = None, thread_id: str = '', timestamp: datetime = None, properties: dict = None):
        self.id = id or str(uuid.uuid4())
        self.thread_id = thread_id
        self.timestamp = timestamp or datetime.utcnow()
        self.properties = properties or {}
