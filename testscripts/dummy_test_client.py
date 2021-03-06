# -*- coding: utf-8 -*-


"""Simulates test run: generates a sequence of events
   and sends these events to the purkinje server
"""

import logging
import time
from purkinje import message
import websocket
import sys


# Interval between messages (in seconds)
MSG_COUNT = 500
MSG_INTERVAL = 0


def setup_logging():
    logging.basicConfig(
        format='%(levelname)s:%(message)s', level=logging.DEBUG)


if __name__ == '__main__':
    setup_logging()

    if len(sys.argv) != 2:
        raise Exception(
            'Usage: {} <websocket URL>\nExample URL: {}'.format(
                __file__,
                'ws://localhost:5000/event'))
    websocket_url = sys.argv[1]

    ws = websocket.create_connection(websocket_url)

    # TODO: flesh out; use actual sequence including information
    # about project / test suite

    for i in range(MSG_COUNT):
        event = message.TestCaseStartEvent('dummy_client msg #{}'.format(i))
        ws.send(event.serialize())
        time.sleep(MSG_INTERVAL)

    ws.send(message.ConnectionTerminationEvent().serialize())
