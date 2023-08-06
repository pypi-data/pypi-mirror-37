# ickafka

A kafka consumer with color.

[![Build Status](https://travis-ci.org/davegallant/ickafka.svg?branch=master)](https://travis-ci.org/davegallant/ickafka)

![ickafka_demo](https://user-images.githubusercontent.com/4519234/44621701-d6516300-a878-11e8-8ab7-752e7b286352.gif)

## Installation

```bash
pip install ickafka
```

## Usage

Start a consumer at the latest offset:

```bash
ickafka -s localhost -t my_test_topic
```

To specify a consumer group name (default is None):

```bash
ickafka -s localhost -t my_test_topic -g testgroup
```

Consume all messages from the earliest offset:

```bash
ickafka -s localhost -t my_test_topic -o earliest
```
