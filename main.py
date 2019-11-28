from LightController import LightController
import http.server
import socketserver
import os
import websockets
import asyncio
import json
import signal
import sys

from multiprocessing import Process

import datetime
import random

# from ClapListener import ClapListsner

light_controller = LightController()

def setup_light_controller():
    global light_controller

    light_controller.add_lights({
        'LED_1': 4,
        'LED_2': 7,
        'LED_3': 8,
    })

    light_controller.turn_on_lights([4])
    #
    # light_controller.turn_off_lights([17])

def setup_web_server():
    os.chdir('./public')

    PORT = 9000

    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()

def setup_ws_server(light_controller):

    async def time(websocket, path):
        while True:
            packet = json.dumps(light_controller.list_lights())
            await websocket.send(packet)
            await asyncio.sleep(400)

    start_server = websockets.serve(time, "127.0.0.1", 5678)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


def signal_handler(sig, frame):
    global light_controller
    light_controller._release_lights()
    sys.exit(0)

def run():
    global light_controller

    signal.signal(signal.SIGINT, signal_handler)

    setup_light_controller()

    p = Process(target=setup_ws_server, args=(light_controller,))
    p.start()

    setup_web_server()

run();
