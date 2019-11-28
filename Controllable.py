class Controllable:

    owner = None
    name = None
    state = None

    def __init__(self, owner, name):

        if(not (name and owner and callable(getattr(owner, 'emit', None)))):
             raise Exception('name and owner are required')

        self.name = name
        self.owner = owner

    def emit(self):
        self.owner.emit(self.name, self.state)
