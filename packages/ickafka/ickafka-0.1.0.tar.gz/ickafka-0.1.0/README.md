# ickafka

A kafka consumer with color.

[![Build Status](https://travis-ci.org/davegallant/ickafka.svg?branch=master)](https://travis-ci.org/davegallant/ickafka)

![ickafka_demo](https://user-images.githubusercontent.com/4519234/47335349-d55e6700-d658-11e8-9552-260c56caa696.gif)

## Installation

```bash
pip install ickafka
```

## Usage

Start consuming at the latest offset:

```bash
ickafka -s localhost:9092 -t my_test_topic
```

To specify a consumer group name (default is None):

```bash
ickafka -s localhost:9092 -t my_test_topic -g testgroup
```

Consume all messages from the earliest offset:

```bash
ickafka -s localhost:9092 -t my_test_topic -o earliest
```

Capture all consumed messages into a json file:

```bash
ickafka -s localhost:9092 -t my_test_topic --capture
```

Disabling color:

```bash
ickafka -s localhost:9092 -t my_test_topic --no-color
```
