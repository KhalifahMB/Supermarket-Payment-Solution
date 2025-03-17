import hashlib
from database import DatabaseManager


class AuthSystem:
    def __init__(self):
        self.db = DatabaseManager()

    def hash_password(self, password: str) -> str:
        # Hashes a password using SHA-256 and returns the hashed password
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self, username: str, password: str) -> dict | None:
        # Attempts to log in a user by verifying their username and password
        query = "SELECT * FROM Users WHERE username = ? AND password = ?"
        hashed_pw = self.hash_password(password)
        # Execute the query with hashed password
        result = self.db.execute_query(
            query, (username, hashed_pw), fetch=True)
        # Return the first result if found, otherwise None
        return result[0] if result else None

    def signup(self, username, password, role):
        hashed_pw = self.hash_password(password)
        self.db.execute_query(
            "INSERT INTO Users (username, password, role) VALUES (?, ?, ?)",
            (username, hashed_pw, role)
        )
