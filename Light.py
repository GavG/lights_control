from Controllable import Controllable

class Light(Controllable):

    ON_STATE = 'on'
    OFF_STATE = 'off'
    FLASHING_STATE = 'flashing'

    ENABLE_COMMAND = '_enable'
    DISABLE_COMMAND = '_disable'
    ON_COMMAND = '_turn_on'
    OFF_COMMAND = '_turn_off'
    FLASH_COMMAND = '_flash'

    VALID_COMMANDS = [ENABLE_COMMAND, DISABLE_COMMAND, ON_COMMAND, OFF_COMMAND, FLASH_COMMAND]
    VALID_PINS = [4, 7, 8, 9, 10, 11, 17, 18, 22, 23, 24, 25, 27]

    DEFAULT_FLASHING_RATE = 200

    pin = None
    flashing_rate = DEFAULT_FLASHING_RATE
    state = OFF_STATE
    enabled = False

    def __init__(self, owner, name, pin):
        if(not (pin and isinstance(pin, int) and pin in self.VALID_PINS)):
            raise Exception('pin is required and must be valid')

        Controllable.__init__(self, owner, name)
        self.pin = pin

    def release(self):
        #free up GPIOs
        print("Release: " + self.name + ' pin: ' + str(self.pin))

    def summary(self):
        return {
            'pin': self.pin,
            'name': self.name,
            'state': self.state,
            'enabled': self.enabled,
        }

    def _update(self):
        if(self.enabled):
            print(str(self.pin) + ' ENABLED ->')
            if(self.state == self.ON_STATE):
                print('LED ON')
            elif(self.state == self.OFF_STATE):
                print('LED OFF')
            elif(self.state == self.FLASHING_STATE):
                print('LED FLAHSING')
        else:
            print(str(self.pin) + ' DISABLED ->')

    async def command(self, command, params = None):
        if(command in self.VALID_COMMANDS):
            getattr(self, command)(params)
            self._update()
            await self.emit()

    def _enable(self, params = None):
        self.enabled = True
        print(self.name + ' is enabled')
        return True

    def _disable(self, params = None):
        self.enabled = False
        print(self.name + ' is disabled')
        return True

    def _turn_on(self, params = None):
        if(self.state != self.ON_STATE):
            print(self.name + ' is on')
            self.state = self.ON_STATE

    def _turn_off(self, params = None):
        if(self.state != self.OFF_STATE):
            print(self.name + ' is off')
            self.state = self.OFF_STATE

    def _flash(self, params = None):
        if(self.state != self.FLASHING_STATE):
            print(self.name + ' is flashing')
            self.state = self.FLASHING_STATE

    def _set_flash_rate(self, params):
        if(isinstance(params, int) and params != self.flashing_rate):
            self.flashing_rate = params.flashing_rate
            print(self.name + ' flash rate updated')
            return True
