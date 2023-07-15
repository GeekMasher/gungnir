"""Dependency Track Project."""
import json
import base64
import logging

from gungnir.dependencytrack.api import DependencyTrack, checkResponse
from gungnir.project import Container, OperatingSystem

logger = logging.getLogger("gungnir.dependencytrack")


class Project:
    """Dependency Track Project."""

    @staticmethod
    def lookup(project: OperatingSystem | Container):
        """Lookup project based on name."""

        if isinstance(project, Container):
            # get all the children
            uuid = project.parent.uuid
            url = f"{DependencyTrack.base}/project/{uuid}/children"
        else:
            url = f"{DependencyTrack.base}/project"

        resp = DependencyTrack.session.get(url, params={"name": project.name})

        jsdata = checkResponse(resp)

        if len(jsdata) == 0:
            return

        for result in jsdata:
            # if parent, look for the child matching the name
            if project.parent and project.name != result.get("name"):
                continue

            project.__dict__.update(result)
            project.active = True

    @staticmethod
    def create(project: OperatingSystem | Container):
        """Create a new Project in DependencyTrack.

        Required access to `PORTFOLIO_MANAGEMENT` permission todo this
        """
        logger.info(f"Creating new project (version: {project.version})")

        parent = None
        if project.parent:
            parent = {"uuid": project.parent.uuid}

        payload = {
            "active": True,
            "classifier": project.classifier,
            "name": project.name,
            "parent": parent,
            "version": project.version,
        }
        resp = DependencyTrack.session.put(
            f"{DependencyTrack.base}/project", json=payload
        )

        data = checkResponse(resp, 201)
        if not isinstance(data, dict):
            return
        project.__dict__.update(**data)

    @staticmethod
    def update(project: OperatingSystem | Container):
        """Update Project in Dependency Track."""
        logger.debug(f"Updating project :: {project.uuid}")

        parent = None
        if project.parent:
            parent = {"uuid": project.parent.uuid}

        payload = {
            "uuid": project.uuid,
            "name": project.name,
            "active": True,
            "classifier": project.classifier,
            "version": project.version,
            "parent": parent,
        }
        resp = DependencyTrack.session.post(
            f"{DependencyTrack.base}/project", json=payload
        )

        checkResponse(resp)
        logger.info("Successfully updated remote Project")

    @staticmethod
    def getChildren(project: OperatingSystem):
        """Get Project children."""
        logger.debug(f"Get Children for :: {project.uuid}")
        resp = DependencyTrack.session.get(
            f"{DependencyTrack.base}/project/{project.uuid}/children"
        )
        data = checkResponse(resp)

        for child in data:
            sha, _ = child.get("version", "1-1").split("-", 1)
            project.containers.append(
                Container(
                    child.get("name", ""),
                    sha,
                    uuid=child.get("uuid"),
                    parent=project,
                    active=bool(child.get("active", False)),
                )
            )

    @staticmethod
    def uploadSbom(project: Container, bom: dict):
        """Upload SBOM to Dependency Track API."""
        b64 = base64.b64encode(json.dumps(bom).encode())
        payload = {"project": project.uuid, "bom": b64.decode()}
        resp = DependencyTrack.session.put(f"{DependencyTrack.base}/bom", json=payload)

        checkResponse(resp)
