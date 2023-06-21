import logging
from typing import Dict, List, Optional

from requests import Session
import requests


logger = logging.getLogger("gungnir.dependencytrack")

KNOWN_ERRORS = {304: ""}


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


def checkResponse(
    resp: requests.Response, expected: int = 200, is_json: bool = True
) -> Dict | List[Dict]:
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
