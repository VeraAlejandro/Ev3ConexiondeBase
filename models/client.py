from models.database import Database

class Client:
    def __init__(self, db: Database):
        self.db = db

    def register(self, client_key, name, email, phone, password):
        self.db.execute("create_client.sql", (client_key, name, email, phone, password))
        print(f"Cliente {name} registrado con éxito!")

    def get_all_clients(self):
        return self.db.query("get_all_clients.sql")

    def update(self, client_id, client_key, name, email, phone):
        self.db.execute("update_client.sql", (client_key, name, email, phone, client_id))
        print(f"Cliente {name} actualizado con éxito!")

    def delete(self, client_id):
        self.db.execute("delete_client.sql", (client_id,))
        print(f"Cliente con ID {client_id} eliminado con éxito!")
