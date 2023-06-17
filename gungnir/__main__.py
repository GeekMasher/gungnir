import os
import logging
import argparse

from gungnir import __title__, __description__, __banner__, __version__
from gungnir.dependencytrack import DependencyTrack
from gungnir.gungnir import Gungnir


logger = logging.getLogger("gungnir")


parser = argparse.ArgumentParser(__title__, description=__description__)
parser.add_argument("--debug", action="store_true", help="Enable Debug mode")
parser.add_argument("--banner", action="store_true", help="Show banner")
parser.add_argument("--version", action="store_true", help="Show version")

parser.add_argument("--container", action="store_true", help="Enable container mode")
parser.add_argument("--disable-banner", action="store_true", help="Disable banner")
parser.add_argument(
    "--hostname",
    default=os.environ.get("HOSTNAME"),
    help="Hostname (mainly for containers)",
)
parser.add_argument(
    "-t",
    "--token",
    default=os.environ.get("DEPENDENCYTRACK_TOKEN"),
    help="DependencyTrack Token",
)
parser.add_argument(
    "-i",
    "--instance",
    default=os.environ.get("DEPENDENCYTRACK_URL"),
    help="DependencyTrack Instance",
)


arguments = parser.parse_args()


if arguments.version:
    print(__version__)
    exit(0)
elif arguments.banner:
    print(__banner__)
    exit(0)

if arguments.container:
    arguments.disable_banner = True

logging.basicConfig(
    level=logging.DEBUG if arguments.debug or os.environ.get("DEBUG") else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

if not arguments.disable_banner:
    print(__banner__, flush=True)

DependencyTrack.init(arguments.instance, arguments.token)
logger.info(
    f"DependencyTrack Instance :: {DependencyTrack.instance} ({DependencyTrack.getVersion()})"
)

gungnir = Gungnir(hostname=arguments.hostname, container=arguments.container)


logger.info(f"Host :: {gungnir.host.name} ({gungnir.host.version})")

logger.info("List of Local Containers:")
for container in gungnir.projects:
    logger.info(f" > Container('{container.name}', '{container.version}')")

logger.info("Processing Containers:")
gungnir.processContainers()

logger.info("Checking Host DependencyTrack Children:")
gungnir.checkHostContainers()

logger.info("Completed!")
