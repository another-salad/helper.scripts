"""Pulls and restarts a container via docker compose (v1 and v2)"""

from typing import Optional

from subprocess import check_call, CalledProcessError
from pathlib import Path

def _send_commands(*args, working_dir: str):
    """
    send all commands from args
    :param working_dir: The DIR to run the cmds from
    :param args: lists ["your"], ["args", "here"], ["please"]
    """
    working_dir = Path(working_dir)
    failing_cmds = []
    for cmd in args:
        try:
            check_call(cmd, cwd=working_dir)
        except CalledProcessError as exc:
            failing_cmds.append([cmd, repr(exc), exc.returncode])
        except FileNotFoundError as exc:  # The directory we provided doesn't exist
            failing_cmds.append([cmd, repr(exc), working_dir])
            break

    if failing_cmds:
        raise Exception(f"The following commands raised an exception: {failing_cmds}")


def pull_restart(working_dir: str, compose_file: Optional[str] = None, v2: bool = True):
    """Pulls the latest image via docker compose. Expects the compose file name to be 'docker-compose.yml' unless
    stated otherwise. Defaults to docker compose v2.
    :param working_dir: The DIR to run the cmds from
    :param compose_file: The name of the compose file to point at
    :param v2: True for docker compose v2 else v1
    """
    if v2:
        compose_cmd = ["/usr/bin/docker", "compose"]
    else:
        # Depending on your distro of choice (yes I am assuming Linux here...) we may be in /usr/local/bin or just /usr/bin
        path_options = ["/usr/local/bin/docker-compose", "/usr/bin/docker-compose"]
        for po in path_options:
            if Path(po).exists():
                compose_cmd = [po]  # python, you are a pain in my arse...
                break
        else:
            # Crash and burn because _python_
            raise Exception("Unable to find docker compose v1 path. Is it installed?")

    # This whole thing is a hack, so lets add more.
    if compose_file:
        compose_cmd.extend(["-f", compose_file])

    pull = [*compose_cmd, "pull"]
    down = [*compose_cmd, "down", "--remove-orphans"]
    up = [*compose_cmd, "up", "-d"]
    _send_commands(*(pull, down, up), working_dir=working_dir)
