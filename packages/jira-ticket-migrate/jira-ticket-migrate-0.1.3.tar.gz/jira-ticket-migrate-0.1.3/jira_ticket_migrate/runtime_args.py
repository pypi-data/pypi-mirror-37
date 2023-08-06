"""Contains functions to parse runtime arguments."""

import argparse
import os.path
from .version import DESCRIPTION, NAME, VERSION

CONFIG_FILE_NAME = "config.yaml"


def parse_runtime_args() -> argparse.Namespace:
    """Parse runtime args using argparse.

    Returns:
        An argparse.Namespace containing the runtime arguments as
        attributes.
    """
    # Default config file location
    project_base_dir = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
    default_config_file_path = os.path.join(project_base_dir, CONFIG_FILE_NAME)

    # Main runtime options
    parser = argparse.ArgumentParser(
        prog=NAME, description="%(prog)s - " + DESCRIPTION
    )
    parser.add_argument(
        "-c",
        "--config",
        default=default_config_file_path,
        help="explicit path to config file",
    )
    parser.add_argument(
        "--version", action="version", version="%(prog)s " + VERSION
    )

    return parser.parse_args()
