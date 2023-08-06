"""Parsing of CLI input (args)."""

import argparse
from ickafka.__version__ import version


def get_args():
    """Parse args"""

    parser = argparse.ArgumentParser(description="Consume from kafka")
    parser.add_argument(
        "-s", "--server", help="kafka broker ip or hostname", default="localhost"
    )
    parser.add_argument("-g", "--group", help="kafka consumer group", default=None)
    parser.add_argument(
        "-o",
        "--offset",
        help="which offset to start at. options: smallest, earliest, latest",
        default="latest",
    )
    parser.add_argument("-t", "--topic", help="kafka topic name", required=True)
    parser.add_argument("--capture", dest="capture", action="store_true")
    parser.add_argument("--no-color", dest="no_color", action="store_true")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=version,
        help="ickafka version",
        default=None,
    )
    return parser.parse_args()
