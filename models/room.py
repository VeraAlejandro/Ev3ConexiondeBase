from models.database import Database

class Room:
    def __init__(self, db: Database):
        self.db = db

    def register(self, room_key, name, capacity, schedule, availability, description):
        self.db.execute("create_room.sql", (room_key, name, capacity, schedule, availability, description))

    def get_all_rooms(self):
        return self.db.query("get_all_rooms.sql")

    def update(self, id_room, room_key, name, capacity, schedule, availability, description):
        self.db.execute("update_room.sql", (room_key, name, capacity, schedule, availability, description, id_room))

    def delete(self, id_room):
        self.db.execute("delete_room.sql", (id_room,))
