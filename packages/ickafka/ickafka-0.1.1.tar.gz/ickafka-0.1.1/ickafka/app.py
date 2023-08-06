"""Improved Color Kafka"""

import argparse
import atexit
import json
import os
import os.path
import sys
from datetime import datetime
from kafka import KafkaConsumer
from pygments import highlight
from pygments.formatters import TerminalFormatter  # pylint: disable-msg=E0611
from pygments.lexers import JsonLexer  # pylint: disable-msg=E0611
from ickafka.__version__ import version


CAPTURED_MESSAGES = []


def create_home_directory_folder():
    """Creates a folder named .ickafka in user's home directory"""
    home_directory = os.path.expanduser("~")
    if not os.path.isdir("%s/.ickafka" % home_directory):
        os.mkdir(os.path.join(home_directory, ".ickafka"))
    if not os.path.isdir("%s/.ickafka/captures" % home_directory):
        os.mkdir(os.path.join(home_directory, ".ickafka/captures"))


def get_args():
    """Parse args using argparse"""

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


def start_consumer(arguments):

    # start consuming them bytes
    consumer = KafkaConsumer(
        arguments.topic,
        auto_offset_reset=arguments.offset,
        bootstrap_servers=[arguments.server],
        enable_auto_commit=True,
        group_id=arguments.group,
    )

    # print each message that is consumed
    for count, message in enumerate(consumer, 1):
        message = message.value.decode("utf-8")
        try:
            message = json.loads(message)
            message = json.dumps(message, indent=4, sort_keys=True)
            if arguments.no_color:
                print(message)
            else:
                print(highlight(message, JsonLexer(), TerminalFormatter()))
            CAPTURED_MESSAGES.append(json.loads(message))
        except Exception:  # pylint: disable=broad-except
            print(message)
            CAPTURED_MESSAGES.append(message)
        print("messages consumed: {}".format(count))
        print("")


def exit_handler():
    print("")
    print("Shutting down consumer...")
    # If there are captured messages and the capture flag is set to true,
    # dump messages as a json array
    if CAPTURED_MESSAGES and USE_CAPTURE:
        json_dumped_file = "{}/.ickafka/captures/{}_{}.json".format(
            os.path.expanduser("~"), KAFKA_TOPIC, datetime.utcnow().isoformat()
        )
        print("")
        print("Dumping consumed messages into: %s" % json_dumped_file)
        print("")
        with open(json_dumped_file, "w") as outfile:
            json.dump(CAPTURED_MESSAGES, outfile, sort_keys=True, indent=4)
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)


atexit.register(exit_handler)

try:
    create_home_directory_folder()
    args = get_args()
    USE_CAPTURE = args.capture
    KAFKA_TOPIC = args.topic
    start_consumer(arguments=args)

except KeyboardInterrupt:
    exit_handler()
