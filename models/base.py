import hashlib
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Any
import logging


class AbstractRole(ABC):
    """Abstract base class for all user roles"""

    def __init__(self, user_id: int, full_name: str, email: str, password: str):
        self._id = user_id
        self._full_name = full_name
        self._email = email
        self._password_hash = self._hash_password(password)
        self._created_at = datetime.now().isoformat()

    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password: str) -> bool:
        """Verify password against stored hash"""
        return self._hash_password(password) == self._password_hash

    @abstractmethod
    def get_profile(self) -> Dict[str, Any]:
        """Get user profile information"""
        pass

    @abstractmethod
    def update_profile(self, **kwargs) -> bool:
        """Update user profile"""
        pass


class User(AbstractRole):
    """Base user class with common functionality"""

    def __init__(self, user_id: int, full_name: str, email: str, password: str, role: str):
        super().__init__(user_id, full_name, email, password)
        self.role = role
        self._notifications: List[Dict] = []
        self.phone = ""
        self.address = ""

    def add_notification(self, message: str, priority: str = "normal") -> None:
        """Add notification to the user"""
        notification = {
            'id': len(self._notifications) + 1,
            'message': message,
            'created_at': datetime.now().isoformat(),
            'is_read': False,
            'priority': priority
        }
        self._notifications.append(notification)
        logging.info(f"Notification added for user {self._id}: {message}")

    def view_notifications(self) -> List[Dict]:
        """View all notifications"""
        return sorted(self._notifications, key=lambda x: x['priority'] == 'high', reverse=True)

    def delete_notification(self, notification_id: int) -> bool:
        """Delete notification by ID"""
        for i, notif in enumerate(self._notifications):
            if notif['id'] == notification_id:
                del self._notifications[i]
                return True
        return False

    def get_profile(self) -> Dict[str, Any]:
        """Get user profile"""
        return {
            'id': self._id,
            'full_name': self._full_name,
            'email': self._email,
            'role': self.role,
            'created_at': self._created_at,
            'phone': self.phone,
            'address': self.address
        }

    def update_profile(self, **kwargs) -> bool:
        """Update user profile"""
        for key, value in kwargs.items():
            if hasattr(self, key) and not key.startswith('_'):
                setattr(self, key, value)
        return True