"""Improved Color Kafka"""

import atexit
import json
import os
import sys
from datetime import datetime
from kafka import KafkaConsumer
from pygments import highlight
from pygments.formatters import TerminalFormatter  # pylint: disable-msg=E0611
from pygments.lexers import JsonLexer  # pylint: disable-msg=E0611
from ickafka.config import create_config_dir, CAPTURES_FOLDER
from ickafka.input import get_args

args = get_args()
messages_captured = []


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
            messages_captured.append(json.loads(message))
        except Exception:  # pylint: disable=broad-except
            print(message)
            messages_captured.append(message)
        print("messages consumed: {}".format(count))
        print("")


def exit_handler():
    if not args.version:
        print("")
        print("Shutting down consumer...")
    # If there are captured messages and the capture flag is set to true,
    # dump messages as a json array
    if messages_captured and args.capture:
        json_dumped_file = "{}/{}_{}.json".format(
            CAPTURES_FOLDER, args.topic, datetime.utcnow().isoformat()
        )
        print("")
        print("Dumping consumed messages into: %s" % json_dumped_file)
        print("")
        with open(json_dumped_file, "w") as outfile:
            json.dump(messages_captured, outfile, sort_keys=True, indent=4)
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)


atexit.register(exit_handler)

try:
    create_config_dir()
    start_consumer(arguments=args)

except KeyboardInterrupt:
    exit_handler()
