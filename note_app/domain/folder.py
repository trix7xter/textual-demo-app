from dataclasses import dataclass


@dataclass
class Folder:
    name: str
    path: str

    def __post_init__(self):
        if not self.name or self.name.strip() == "":
            raise ValueError("Folder must have name")
