from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class Note:
    name: str
    path: Path
    content: Optional[str] = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if not self.name or self.name.strip() == "":
            raise ValueError("Note must have name")
