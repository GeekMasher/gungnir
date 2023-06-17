import os
import logging
import argparse

from gungnir import __title__, __description__, __banner__
from gungnir.dependencytrack import DependencyTrack
from gungnir.gungnir import Gungnir


logger = logging.getLogger("gungnir")


parser = argparse.ArgumentParser(__title__, description=__description__)
parser.add_argument("--debug", action="store_true")

parser.add_argument("-t", "--token", default=os.environ.get("DEPENDENCYTRACK_TOKEN"))
parser.add_argument("-i", "--instance", default=os.environ.get("DEPENDENCYTRACK_URL"))


arguments = parser.parse_args()

logging.basicConfig(
    level=logging.DEBUG if arguments.debug or os.environ.get("DEBUG") else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

print(__banner__)

DependencyTrack.init(arguments.instance, arguments.token)

gungnir = Gungnir()


print(f"Host :: {gungnir.host.name} ({gungnir.host.version})\n")

print("List of Local Containers:\n")
for container in gungnir.projects:
    print(f" > Container('{container.name}', '{container.version}')")

print("\nProcessing Containers:\n")
gungnir.processContainers()

print("\nChecking Host DependencyTrack Children:\n")
gungnir.checkHostContainers()

