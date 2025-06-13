from datetime import datetime
from typing import List
import uuid

class Thread:
    def __init__(self, id: str = None, capsule_id: str = '', name: str = '', tags: List[str] = None, created_at: datetime = None):
        self.id = id or str(uuid.uuid4())
        self.capsule_id = capsule_id
        self.name = name
        self.tags = tags or []
        self.created_at = created_at or datetime.utcnow()
        self.entries: List['Entry'] = []
