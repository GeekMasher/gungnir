"""Dependency Track module."""

import logging
from typing import Dict, List
from requests import Session, Response


logger = logging.getLogger("gungnir.dependencytrack")

KNOWN_ERRORS = {304: ""}


class DependencyTrack:
    """Dependency Track API class."""

    base: str
    """Full base URL"""
    instance: str = "http://localhost:8080"
    """Instance"""
    token: str = ""
    """Token"""
    version: str = "v1"
    """Version number"""

    session: Session
    """Requests Session"""

    @staticmethod
    def init(instance: str, token: str) -> None:
        """Initialise Dependency Track API."""
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
        """Get Version."""
        resp = DependencyTrack.session.get(f"{DependencyTrack.instance}/api/version")
        return resp.json().get("version", "NA")


def checkResponse(
    resp: Response, expected: int = 200, is_json: bool = True
) -> Dict | List[Dict]:
    """Check Response."""
    if resp.status_code == expected:
        if is_json:
            return resp.json()
        return {}

    err = KNOWN_ERRORS.get(resp.status_code)
    if err:
        logger.error(err)
        raise Exception(err)
    logger.error(f"Response Status Code :: {resp.status_code}")
    logger.error(f"Response Content :: {resp.content}")
    raise Exception(f"Unknown error")
