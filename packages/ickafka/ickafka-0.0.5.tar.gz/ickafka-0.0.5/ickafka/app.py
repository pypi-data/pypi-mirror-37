"""Improved Color Kafka"""

import argparse
import json
from kafka import KafkaConsumer
from pygments import highlight
from pygments.formatters import TerminalFormatter  # pylint: disable-msg=E0611
from pygments.lexers import JsonLexer  # pylint: disable-msg=E0611


def main():
    # parse the args
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
    args = parser.parse_args()

    # start consuming them bytes
    consumer = KafkaConsumer(
        args.topic,
        auto_offset_reset=args.offset,
        bootstrap_servers=[args.server],
        enable_auto_commit=True,
        group_id=args.group,
    )

    # print each message that is consumed
    for count, message in enumerate(consumer, 1):
        try:
            message = message.value.decode("utf-8")
            message = json.loads(message)
            message = json.dumps(message, indent=4, sort_keys=True)
            print(highlight(message, JsonLexer(), TerminalFormatter()))
        except Exception:  # pylint: disable=broad-except
            print(message)
        print("message count: {}".format(count))


main()
