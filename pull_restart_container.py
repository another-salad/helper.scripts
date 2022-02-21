"""Pulls the latest image and restarts the container for the docker-compose.yml file in the provided directory"""

from argparse import ArgumentParser

from common.compose_pull_restart import pull_restart


class Args(ArgumentParser):
    """Arg parser"""

    def __init__(self, description="Pulls and restarts the container spawned via docker compose in the provided DIR"):
        super().__init__(description=description)
        self.add_argument("--dir", dest="working_dir", type=str)
        self.add_argument("--v1", dest="v2", action="store_false")
        self.set_defaults(v2=True)


def main():
    """Main baby"""
    args = Args().parse_args()
    pull_restart(args.working_dir, args.v2)


if __name__ == "__main__":
    main()
