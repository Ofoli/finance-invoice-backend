import subprocess
import logging

from app.core.constants import APP_LOGGER

logger = logging.getLogger(APP_LOGGER)


def ssh_secure_copy(src: str, dst: str) -> bool:
    command: list[str] = ["scp", src, dst]
    try:
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError as e:
        logger.error("Command:{} failed: {}".format(command, e))
        return False
