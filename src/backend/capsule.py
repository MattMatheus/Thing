from datetime import datetime
from typing import List, Optional
import uuid

class Capsule:
    def __init__(self, id: str = None, name: str = '', description: Optional[str] = None, created_at: datetime = None):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.description = description
        self.created_at = created_at or datetime.utcnow()
        self.threads: List['Thread'] = []
