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
        print(f"User {name} registered successfully!")