"""Gungnir."""
import logging
import platform
from typing import List

import docker

from gungnir.dependencytrack.project import Project
from gungnir.syft import Syft
from gungnir.project import OperatingSystem, Container

logger = logging.getLogger("gungnir.gungnir")


class Gungnir:
    """Gungnir class."""

    def __init__(self, hostname: str, container: bool = False) -> None:
        """Initialise Gungnir."""
        self.active_projects = []
        self.client = docker.from_env()
        self.syft = Syft()

        # host
        self.host = OperatingSystem(hostname)
        Project.lookup(self.host)

        logger.debug(f"Host Project :: {self.host}")

        if not self.host.uuid:
            Project.create(self.host)

        if not container:
            host_version = f"{platform.system()}-{platform.release()}"
            if self.host.version != host_version:
                self.host.platform = host_version
                Project.update(self.host)

        # host remote containers
        Project.getChildren(self.host)
        logger.info(f"Host Sub-projects :: {len(self.host.containers)}")

        self.projects = self.generateProjects()

    def generateProjects(self) -> List[Container]:
        """Generate the Projects."""
        projects = []
        for container in self.client.containers.list():
            name = container.name
            version = container.image.short_id

            self.active_projects.append(name)

            project = next(
                (s for s in self.host.containers if s.name == name),
                Container(name, "1", parent=self.host),
            )

            # create a new project
            if not project.active:
                Project.create(project)

            # re-activate project
            if not project.active:
                logger.info(f"Activating Project :: {project.name}")
                project.active = True
                Project.update(project)

            projects.append(project)

        return projects

    def processContainers(self):
        """Process Container."""
        for project in self.projects:
            container = self.client.containers.get(project.name)
            sha = container.image.short_id
            image_id = container.image.id

            version = f"{sha}-{project.parent.name}"
            logger.info(f"Processing container :: {project.name} ({version})")
            logger.debug(f"Checking Versions :: {project.version} -> {version}")

            if project.version != version:
                # upload BOM only if version is new / different
                logger.info(f"Remote version is different to local :: {version}")

                bom = self.syft.generateSBOM(image_id, project.name)

                logger.info("Uploading BOM to remote DependencyTrack")
                Project.uploadSbom(project, bom)

                # once uploaded, update version to match
                project.sha = version
                Project.update(project)

            else:
                logging.debug(
                    f"Same version used since last process :: {project.version}"
                )

    def checkHostContainers(self):
        """Check Host Containers."""
        for project in self.host.containers:
            if project.name in self.active_projects:
                logging.debug(f"Project active :: {project}")
                continue

            if project.active:
                # deactivate project
                logging.warning(f"Deactivating Projects as offline :: {project}")
                project.active = False
                Project.update(project)
