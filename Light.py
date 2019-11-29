from Controllable import Controllable

class Light(Controllable):

    ON_STATE = 'on'
    OFF_STATE = 'off'
    FLASHING_STATE = 'flashing'

    ON_COMMAND = '_turn_on'
    OFF_COMMAND = '_turn_off'
    FLASH_COMMAND = '_flash'

    VALID_COMMANDS = [ON_COMMAND, OFF_COMMAND, FLASH_COMMAND]
    VALID_PINS = [4, 7, 8, 9, 10, 11, 17, 18, 22, 23, 24, 25, 27]

    COMMAND_RESULTANT_STATES = {
        ON_COMMAND: ON_STATE,
        OFF_COMMAND: OFF_STATE,
        FLASH_COMMAND: FLASHING_STATE
    }

    DEFAULT_FLASHING_RATE = 200

    pin = None
    flashing_rate = DEFAULT_FLASHING_RATE
    state = OFF_STATE

    def __init__(self, owner, name, pin):
        if(not (pin and isinstance(pin, int) and pin in self.VALID_PINS)):
            raise Exception('pin is required and must be valid')

        Controllable.__init__(self, owner, name)
        self.pin = pin

    def release(self):
        #free up GPIOs
        print("Release: " + self.name + ' pin: ' + str(self.pin))

    async def command(self, command, params = None):

        if(not command in self.VALID_COMMANDS):
            return false

        if(getattr(self, command)(params)):
            self.state = self.COMMAND_RESULTANT_STATES[command]

        await self.emit()

    def _turn_on(self, params = None):
        if(self.state != self.COMMAND_RESULTANT_STATES[self.ON_COMMAND]):
            print(self.name + ' is on')
            return True

    def _turn_off(self, params = None):
        if(self.state != self.COMMAND_RESULTANT_STATES[self.OFF_COMMAND]):
            print(self.name + ' is off')
            return True

    def _flash(self, params = None):
        if(self.state != self.COMMAND_RESULTANT_STATES[self.FLASH_COMMAND]):
            print(self.name + ' is flashing')
            return True

    def _set_flash_rate(self, params = None):
        if(isinstance(params, int) and params != self.flashing_rate):
            print(self.name + ' flash rate updated')
            return True
