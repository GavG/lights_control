from LightController import LightController
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

setup_light_controller()
