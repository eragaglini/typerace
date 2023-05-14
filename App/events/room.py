import uuid


class Room:
    def __init__(self, name):
        self.id = str(uuid.uuid4())[:5]
        self.name = name
        self.users_num = 0
