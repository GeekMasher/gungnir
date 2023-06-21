import platform
from typing import Optional, List
from dataclasses import dataclass, field


@dataclass
class OperatingSystem:
    name: str
    platform: str = platform.release()
    # deptrack id
    uuid: Optional[str] = None

    containers: List["Container"] = field(default_factory=list)

    active: bool = False

    def __post_init__(self):
        return

    @property
    def parent(self):
        return None

    @property
    def version(self) -> str:
        return self.platform

    @property
    def classifier(self) -> str:
        return "OPERATING_SYSTEM"


@dataclass
class Container:
    name: str
    sha: str
    # parent
    parent: "OperatingSystem"
    # deptrack id
    uuid: Optional[str] = None

    active: bool = False

    @property
    def version(self) -> str:
        return f"{self.sha}-{self.parent.name}"

    @property
    def classifier(self) -> str:
        return "CONTAINER"
