from Light import Light
from multiprocessing import Value
import json

class LightController:

    lights = {};
    websocket = None

    VALID_COMMANDS = [
        'enable_lights',
        'disable_lights',
        'turn_on_lights',
        'turn_off_lights',
        'flash_lights',
    ]

    def _release_lights(self):
        for light in self.lights.values():
            light.release()

        self.lights = {} #releases refs automagically

    def add_lights(self, lights):
        for name, pin in lights.items():
            self._add_light(name, pin)

    def _add_light(self, name, pin):
        if(not pin in self.lights):
            self.lights[pin] = Light(self, name, pin)
            return True

    def list_lights(self):
        return [light.summary() for light in self.lights.values()]

    async def command(self, command, pins):
        if(command in self.VALID_COMMANDS):
            await getattr(self, command)(pins)

    async def enable_lights(self, pins):
        if(all(pin in self.lights for pin in pins)):
            for pin in pins:
                await self.lights[pin].command(Light.ENABLE_COMMAND)

    async def disable_lights(self, pins):
        if(all(pin in self.lights for pin in pins)):
            for pin in pins:
                await self.lights[pin].command(Light.DISABLE_COMMAND)

    async def turn_on_lights(self, pins):
        if(all(pin in self.lights for pin in pins)):
            for pin in pins:
                await self.lights[pin].command(Light.ON_COMMAND)

    async def turn_off_lights(self, pins):
        if(all(pin in self.lights for pin in pins)):
            for pin in pins:
                await self.lights[pin].command(Light.OFF_COMMAND)

    async def flash_lights(self, pins):
        if(all(pin in self.lights for pin in pins)):
            for pin in pins:
                await self.lights[pin].command(Light.FLASH_COMMAND)

    def set_ws(self, websocket):
        self.websocket = websocket

    async def emit(self, summary):
        if(self.websocket):
            await self.websocket.send(json.dumps({
                'update': summary
            }))
