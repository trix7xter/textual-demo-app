from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Note:
    name: str
    path: str
    content: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    def __post_init__(self):
        if not self.name or self.name.strip() == "":
            raise ValueError("Note must have name")
