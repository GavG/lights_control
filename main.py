from LightController import LightController
import http.server
import socketserver
import os
import websockets
import asyncio
import json
import signal
import sys
import time

import threading


# from ClapListener import ClapListsner

def setup_web_server():
    os.chdir('./public')

    PORT = 9001

    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()

def setup_ws_server(loop):
    global light_controller

    asyncio.set_event_loop(loop)

    async def ws_emit(websocket, data):
        await websocket.send(data)

    async def ws_light_control(websocket, path):

        light_controller.set_ws(websocket)

        await ws_emit(websocket, json.dumps(light_controller.list_lights()))

        async for message in websocket:
            data = json.loads(message)
            if "command" in data:
                print(data["command"])
                await light_controller.command(data["command"], data["pins"])

    start_server = websockets.serve(ws_light_control, "127.0.0.1", 5678)

    loop.run_until_complete(start_server)
    loop.run_forever()


def signal_handler(sig, frame):
    global light_controller
    light_controller._release_lights()
    sys.exit(0)

async def run():
    global light_controller

    signal.signal(signal.SIGINT, signal_handler)

    light_controller = LightController()

    light_controller.add_lights({
        'LED_1': 4,
        'LED_2': 7,
        'LED_3': 8,
    })

    await light_controller.enable_lights([4, 7, 8])

    loop = asyncio.new_event_loop()
    ws_server_thread = threading.Thread(target=setup_ws_server, name='ws', args=[loop])
    ws_server_thread.start()

    web_server_thread = threading.Thread(target=setup_web_server, name='web')
    web_server_thread.start()


asyncio.run(run())
