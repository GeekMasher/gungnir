from dataclasses import dataclass, asdict, field
import json
import logging
from typing import Any, Dict, List, Optional
from base64 import b64encode
from requests.sessions import Session

logger = logging.getLogger("gungnir.dependencytrack")


class DependencyTrack:
    base: str
    instance: str = "http://localhost:8080"
    token: str = ""
    version: str = "v1"

    session: Session

    @staticmethod
    def init(instance: str, token: str) -> None:
        DependencyTrack.instance = instance
        DependencyTrack.version = "v1"

        DependencyTrack.session = Session()
        DependencyTrack.session.headers = {
            "Accepts": "application/json",
            "X-Api-Key": token,
        }

        DependencyTrack.base = (
            f"{DependencyTrack.instance}/api/{DependencyTrack.version}"
        )

    @staticmethod
    def getVersion() -> str:
        resp = DependencyTrack.session.get(f"{DependencyTrack.instance}/api/version")
        return resp.json().get("version", "NA")


@dataclass
class Project:
    name: str
    version: str = ""
    uuid: str = ""
    active: bool = False
    parent: Optional["Project"] = None

    lastInheritedRiskScore: int = 0

    lastBomImport: str = ""
    lastBomImportFormat: str = ""

    classifier: str = "APPLICATION"

    tags: List[Dict[str, str]] = field(default_factory=list)

    metrics: Dict[Any, Any] = field(default_factory=dict)

    present: bool = field(init=False, repr=False, default=False)

    def __post_init__(self):
        self.lookup()

    def toDict(self) -> dict:
        data = asdict(self)
        data.pop("present")
        return data

    def lookup(self):
        url = f"{DependencyTrack.base}/project"
        resp = DependencyTrack.session.get(url, params={"name": self.name})
        if resp.status_code == 404:
            self.present = False
            return

        jsdata = resp.json()
        if len(jsdata) == 0:
            self.present = False
        else:
            self.__dict__.update(jsdata[0])
            self.present = True

    def create(self):
        """Create a new Project in DependencyTrack

        Required access to `PORTFOLIO_MANAGEMENT` permission todo this
        """
        parent = {}
        if self.parent:
            parent["uuid"] = self.parent.uuid

        resp = DependencyTrack.session.put(
            f"{DependencyTrack.base}/project",
            json={
                "active": True,
                "classifier": self.classifier,
                "name": self.name,
                "parent": parent,
                "tags": self.tags,
                "version": self.version,
            },
        )

        if resp.status_code == 403:
            logger.warning("Unable to create Project")
            return
        if resp.status_code != 201:
            print(resp.status_code)
            print(resp.content)
            raise Exception("Failed to create Project")

        # TODO: does `resp.json()` have all the things we need
        self.lookup()

    def update(self):
        """Update Project in Dependency Track"""
        resp = DependencyTrack.session.post(
            f"{DependencyTrack.base}/project", json=self.toDict()
        )

        if resp.status_code != 200:
            print(resp.status_code)
            print(resp.content)
            raise Exception("Failed to update Project")

        logger.info("Successfully updated remote Project")

    def getChildren(self) -> List["Project"]:
        """Get Project children"""
        resp = DependencyTrack.session.get(
            f"{DependencyTrack.base}/project/{self.uuid}/children"
        )
        if resp.status_code != 200:
            print(resp.status_code)
            print(resp.content)
            raise Exception("Failed to get Project children")

        children = []
        for child in resp.json():
            proj = Project(**child)
            children.append(proj)

        return children

    def deactivate(self):
        self.active = False
        self.update()

    def uploadSbom(self, bom: dict):
        b64 = b64encode(json.dumps(bom).encode())
        resp = DependencyTrack.session.put(
            f"{DependencyTrack.base}/bom",
            json={"project": self.uuid, "bom": b64.decode()},
        )

        if resp.status_code != 200:
            print(resp.status_code)
            print(resp.content)
            raise Exception("Failed to upload SBOM")
