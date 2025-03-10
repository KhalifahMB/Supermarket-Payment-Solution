import hashlib
from database import DatabaseManager


class AuthSystem:
    def __init__(self):
        self.db = DatabaseManager()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self, username, password):
        query = "SELECT * FROM Users WHERE username = ? AND password = ?"
        hashed_pw = self.hash_password(password)
        result = self.db.execute_query(
            query, (username, password), fetch=True)
        return result[0] if result else None
