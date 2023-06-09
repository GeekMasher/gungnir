import json
import logging
import os
import argparse
import platform

import docker

from gungnir import __title__, __description__
from gungnir import dependencytrack
from gungnir.dependencytrack import DependencyTrack, Project
from gungnir.syft import Syft

parser = argparse.ArgumentParser(__title__, description=__description__)
parser.add_argument("--debug", action="store_true")

parser.add_argument("-t", "--token", default=os.environ.get("DEPENDENCYTRACK_TOKEN"))
parser.add_argument("-i", "--instance", default=os.environ.get("DEPENDENCYTRACK_URL"))


class Gungnir:
    def __init__(self) -> None:
        self.client = docker.from_env()


arguments = parser.parse_args()

logging.basicConfig(
    level=logging.DEBUG if arguments.debug or os.environ.get("DEBUG") else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

gungnir = Gungnir()
DependencyTrack.init(arguments.instance, arguments.token)

host_project = Project(platform.node())

# syft = Syft()

if not host_project:
    print(f"Root Device project '{hostname}' must be present")
    exit(1)

for container in gungnir.client.containers.list():
    name = container.name
    image_id = container.image.id
    version = container.image.short_id

    if name != "homeassistant":
        continue

    print(f"Container('{name}', '{version}')")

    project = Project(name)
    if not project.active:
        raise Exception("RIP")

    with open("/tmp/gungnir/homeassistant.json") as handle:
        bom = json.load(handle)

    project.uploadSbom(bom)
