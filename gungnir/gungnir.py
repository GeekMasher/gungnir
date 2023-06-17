import logging
import platform
from typing import List

import docker

from gungnir.syft import Syft
from gungnir.dependencytrack import Project


class Gungnir:
    def __init__(self) -> None:
        self.active_projects = []
        self.client = docker.from_env()
        self.syft = Syft()

        # host
        self.host = Project(platform.node())
        host_version = f"{platform.system()}-{platform.release()}"
        if self.host.version != host_version:
            self.host.version = host_version
            self.host.update()

        self.projects = self.generateProjects()

    def generateProjects(self) -> List[Project]:
        projects = []
        for container in self.client.containers.list():
            name = container.name
            version = container.image.short_id

            self.active_projects.append(name)

            project = Project(name, parent=self.host)

            # create a new project
            if not project.present:
                project.version = version
                project.classifier = "CONTAINER"
                project.create()

            projects.append(project)

        return projects

    def processContainers(self):
        for project in self.projects:
            container = self.client.containers.get(project.name) 
            version = container.image.short_id
            image_id = container.image.id

            logging.info(f"Processing container :: {project.name}")

            if project.version != version:
                # upload BOM only if version is new / different
                logging.info("Remote version is different to local, generating BOM")
                bom = self.syft.generateSBOM(image_id, name)
                logging.info("Uploading BOM to remote DependencyTrack")
                project.uploadSbom(bom)

    def checkHostContainers(self):
        for project in self.host.getChildren():
            if project.name in self.active_projects:
                logging.debug(f"Project active :: {project}")
                continue
            
            if project.active:
                # deactivate project
                logging.warning(f"Deactivating Projects as offline :: {project}")
                project.deactivate()

