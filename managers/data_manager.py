from typing import Dict, Optional
from models.users import User, Student, Teacher, Parent, Admin
from models.entities import Assignment, Grade, Schedule, Notification

# DataManager class content

class DataManager:
    """Manages in-memory data storage and operations"""

    def __init__(self):
        self.users: Dict[int, User] = {}
        self.students: Dict[int, Student] = {}
        self.teachers: Dict[int, Teacher] = {}
        self.parents: Dict[int, Parent] = {}
        self.admins: Dict[int, Admin] = {}
        self.assignments: Dict[int, Assignment] = {}
        self.grades: Dict[int, Grade] = {}
        self.schedules: Dict[int, Schedule] = {}
        self.notifications: Dict[int, Notification] = {}
        self._next_id = 1

    def get_next_id(self) -> int:
        """Get next available ID"""
        current_id = self._next_id
        self._next_id += 1
        return current_id

    def add_user(self, user: User) -> bool:
        """Add user to appropriate storage"""
        self.users[user._id] = user

        if isinstance(user, Student):
            self.students[user._id] = user
        elif isinstance(user, Teacher):
            self.teachers[user._id] = user
        elif isinstance(user, Parent):
            self.parents[user._id] = user
        elif isinstance(user, Admin):
            self.admins[user._id] = user

        return True

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Find user by email"""
        for user in self.users.values():
            if user._email == email:
                return user
        return None

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        user = self.get_user_by_email(email)
        if user and user.verify_password(password):
            return user
        return None