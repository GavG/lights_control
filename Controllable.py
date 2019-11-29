class Controllable:

    owner = None
    name = None
    state = None

    def __init__(self, owner, name):

        if(not (name and owner and callable(getattr(owner, 'emit', None)))):
             raise Exception('name and owner are required')

        self.name = name
        self.owner = owner

    def computed_state(self):
        return {
            'state': self.state,
        }

    async def emit(self):
        await self.owner.emit(self.name, self.computed_state())
