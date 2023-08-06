# ickafka

A kafka consumer with color. Name inspired by [icdiff](https://github.com/jeffkaufman/icdiff).

[![Build Status](https://travis-ci.org/davegallant/ickafka.svg?branch=master)](https://travis-ci.org/davegallant/ickafka)
[![PyPI version](https://badge.fury.io/py/ickafka.svg)](https://badge.fury.io/py/ickafka)

![ickafka_gif](https://user-images.githubusercontent.com/4519234/47589203-7d648080-d936-11e8-8b05-b111d75c0ae4.gif)

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
