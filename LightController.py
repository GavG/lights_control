from Light import Light

class LightController:

    lights = {};

    def __init__(self):
        self.add_light('l1', 17)

    def _release_lights(self):
        for light in self.lights.values():
            light.release()

        self.lights = {} #releases refs automagically

    def add_light(self, name, pin):
        if(not pin in self.lights):
            self.lights[pin] = Light(self, name, pin)
            return True

    def list_lights():
        return lights.values()

    def turn_on_lights(self, pins):
        if(all(pin in self.lights for pin in pins)):
            for pin in pins:
                self.lights[pin].command(Light.ON_COMMAND)

    def turn_off_lights(self, pins):
        if(all(pin in self.lights for pin in pins)):
            for pin in pins:
                self.lights[pin].command(Light.OFF_COMMAND)

    def flash_lights(self, pins):
        if(all(pin in self.lights for pin in pins)):
            for pin in pins:
                self.lights[pin].command(Light.FLASH_COMMAND)

    def emit(self, name, state):
        print('light name: ' + name + ', state: ' + state)

def run():

    light_controller = LightController()

    light_controller.turn_on_lights([17])

    light_controller.turn_off_lights([17])

    light_controller._release_lights()

run()
