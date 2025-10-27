from models.database import Database

class User: 
    def __init__(self, db: Database):
        self.db = db
    
    def login(self, email, password):
        result = self.db.query('login_user.sql', (email, password))
        if result:
            return result[0]
        return None
    
    def register(self, name, email, password, type_user):
        self.db.execute('create_user.sql', (name, email, password, type_user))
        print(f"User {name} registrado con éxito!")

    def get_all_user(self):
        return self.db.query("get_all_user.sql")
    
    def update_user(self, user_id, name, email, type_user):
        self.db.execute('update_user.sql', (name, email, type_user, user_id))
        print(f"User {name} actalizado con éxito!")

    def delete_user(self, user_id):
        self.db.execute("delete_user.sql", (user_id,))
        print(f"Usuario con ID {user_id} eliminado.")