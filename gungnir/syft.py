import os
import json
import glob
import tempfile
import logging
import subprocess

logger = logging.getLogger("cdsa.syft")

LOCATIONS = [
    "/usr/local/bin",
    os.path.expanduser("~/.local/bin"),
]
LOCATIONS.extend(glob.glob("/home/linuxbrew/.linuxbrew/Cellar/syft/**/bin"))


class Syft:
    def __init__(self) -> None:
        self.name = "syft"
        self.path = None
        self.storage = os.path.join(tempfile.gettempdir(), "gungnir")

    @property
    def binary(self) -> str:
        if self.path:
            return os.path.join(self.path, self.name)
        return self.name

    def try_command(self, cmd: list[str]) -> bool:
        try:
            with open(os.devnull, "w") as null:
                subprocess.check_call(cmd, stdout=null, stderr=null)
            return True
        except:
            logger.debug("Syft not found on the system")
        return False

    def check(self) -> bool:
        for loc in LOCATIONS:
            logger.debug(f"Checking location :: {loc}")

            fullpath = os.path.join(loc, "syft")

            if os.path.exists(fullpath) or self.try_command([fullpath]):
                self.path = loc
                return True
        return False

    def generateSBOM(self, image: str, name: str) -> dict:
        output = os.path.join(self.storage, f"{name}.json")
        cmd = [self.binary, image, "-o", f"cyclonedx-json={output}"]

        logger.debug(f"SBOM Command :: {cmd}")

        with open(os.devnull, "w") as null:
            subprocess.run(cmd, stdout=null, stderr=null)

        if os.path.exists(output):
            with open(output, "r") as handle:
                return json.load(handle)

        return {}
