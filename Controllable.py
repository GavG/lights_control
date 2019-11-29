class Controllable:

    owner = None
    name = None
    state = None

    def __init__(self, owner, name):

        if(not (name and owner and callable(getattr(owner, 'emit', None)))):
             raise Exception('name and owner are required')

        self.name = name
        self.owner = owner

    def summary(self):
        return {
            'name': self.name,
            'state': self.state,
        }

    async def emit(self):
        await self.owner.emit(self.summary())
