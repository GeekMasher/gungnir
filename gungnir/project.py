"""Gungnir models."""
import platform
from typing import Optional, List
from dataclasses import dataclass, field


@dataclass
class OperatingSystem:
    """Operating System Model."""

    name: str
    """Name."""
    platform: str = platform.release()
    """Platform."""
    # deptrack id
    uuid: Optional[str] = None
    """UUID"""

    containers: List["Container"] = field(default_factory=list)
    """Containers."""

    active: bool = False
    """Active"""

    def __post_init__(self):
        """Post Processing."""
        return

    @property
    def parent(self):
        """Get Parent."""
        return None

    @property
    def version(self) -> str:
        """Get Platform version."""
        return self.platform

    @property
    def classifier(self) -> str:
        """Classifier."""
        return "OPERATING_SYSTEM"


@dataclass
class Container:
    """Container."""

    name: str
    """Name"""
    sha: str
    """SHA"""
    # parent
    parent: "OperatingSystem"
    """Parent Name"""
    # deptrack id
    uuid: Optional[str] = None
    """UUID"""

    active: bool = False
    """Active"""

    @property
    def version(self) -> str:
        """Get version."""
        return f"{self.sha}-{self.parent.name}"

    @property
    def classifier(self) -> str:
        """Classifier."""
        return "CONTAINER"
