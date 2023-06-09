from dataclasses import dataclass, asdict, field
from typing import Optional
from requests.sessions import Session


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


@dataclass
class Project:
    name: str
    version: str = "1"
    uuid: str = ""
    active: bool = False
    parent: Optional["Project"] = None

    tags: list[dict] = field(default_factory=list)
    lastInheritedRiskScore: int = 0
    lastBomImportFormat: str = ""

    classifier: str = "APPLICATION"

    present: bool = field(init=False, repr=False, default=False)

    def __post_init__(self):
        self.lookup()

    def lookup(self):
        url = f"{DependencyTrack.base}/project/lookup"
        resp = DependencyTrack.session.get(
            url, params={"name": self.name, "version": self.version}
        )
        if resp.status_code == 404:
            self.present = False
            return

        self.__dict__ = resp.json()
        self.present = True

    def create(self):
        resp = DependencyTrack.session.put(
            f"{DependencyTrack.base}/project", json=asdict(self)
        )
        if resp.status_code != 200:
            print(resp.status_code)
            print(resp.content)
            raise Exception("Nope")
        return Project(**resp.json())

    def uploadSbom(self, bom: dict):
        req = {"project": asdict(self), "bom": bom}
        resp = DependencyTrack.session.post(
            f"{DependencyTrack.base}/bom", json={"body": req}
        )
