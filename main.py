from LightController import LightController
import http.server
import socketserver
import os
import websockets
import asyncio

from multiprocessing import Process

import datetime
import random

# from ClapListener import ClapListsner

light_controller = LightController()

def setup_light_controller():
    global light_controller

    light_controller.add_lights({
        'l1': 4,
        'l2': 7,
        'l3': 8,
    })

    # light_controller.turn_on_lights([17])
    #
    # light_controller.turn_off_lights([17])

    light_controller._release_lights()

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
            now = datetime.datetime.utcnow().isoformat() + "Z"
            await websocket.send(now)
            await asyncio.sleep(random.random() * 3)

    start_server = websockets.serve(time, "127.0.0.1", 5678)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


def run():
    global light_controller

    setup_light_controller()

    p = Process(target=setup_ws_server, args=(light_controller,))
    p.start()

    setup_web_server()

run();
