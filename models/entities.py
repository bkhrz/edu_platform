from datetime import datetime
from typing import Dict, Any, Union
import logging


class Assignment:
    """Assignment class for managing student tasks"""

    def __init__(self, assignment_id: int, title: str, description: str,
                 deadline: str, subject: str, teacher_id: int, class_id: str,
                 difficulty: str = "medium"):
        self.id = assignment_id
        self.title = title
        self.description = description
        self.deadline = deadline
        self.subject = subject
        self.teacher_id = teacher_id
        self.class_id = class_id
        self.difficulty = difficulty
        self.submissions: Dict[int, str] = {}  # {student_id: content}
        self.grades: Dict[int, int] = {}  # {student_id: grade}

    def add_submission(self, student_id: int, content: str) -> bool:
        """Add student submission"""
        deadline_dt = datetime.fromisoformat(self.deadline)
        if datetime.now() > deadline_dt:
            return False  # Late submission

        self.submissions[student_id] = content
        return True

    def set_grade(self, student_id: int, grade: int) -> bool:
        """Set grade for student"""
        if 1 <= grade <= 5:
            self.grades[student_id] = grade
            return True
        return False

    def get_status(self) -> Dict[str, Any]:
        """Get assignment status"""
        return {
            "id": self.id,
            "title": self.title,
            "submissions": len(self.submissions),
            "graded": len(self.grades),
            "deadline": self.deadline
        }


class Grade:
    """Grade class for managing student grades"""

    def __init__(self, grade_id: int, student_id: int, subject: str,
                 value: int, teacher_id: int, comment: str = ""):
        self.id = grade_id
        self.student_id = student_id
        self.subject = subject
        self.value = value
        self.date = datetime.now().isoformat()
        self.teacher_id = teacher_id
        self.comment = comment

    def update_grade(self, value: int) -> bool:
        """Update grade value"""
        if 1 <= value <= 5:
            self.value = value
            return True
        return False

    def get_grade_info(self) -> Dict[str, Any]:
        """Get grade information"""
        return {
            "id": self.id,
            "student_id": self.student_id,
            "subject": self.subject,
            "value": self.value,
            "date": self.date,
            "teacher_id": self.teacher_id,
            "comment": self.comment
        }


class Schedule:
    """Schedule class for managing class timetables"""

    def __init__(self, schedule_id: int, class_id: str, day: str):
        self.id = schedule_id
        self.class_id = class_id
        self.day = day
        self.lessons: Dict[str, Dict[str, Union[str, int]]] = {}  # {time: {subject, teacher_id}}

    def add_lesson(self, time: str, subject: str, teacher_id: int) -> bool:
        """Add lesson to schedule"""
        if time not in self.lessons:
            self.lessons[time] = {"subject": subject, "teacher_id": teacher_id}
            return True
        return False  # Time slot already occupied

    def view_schedule(self) -> Dict[str, Dict[str, Union[str, int]]]:
        """View complete schedule"""
        return self.lessons

    def remove_lesson(self, time: str) -> bool:
        """Remove lesson from schedule"""
        if time in self.lessons:
            del self.lessons[time]
            return True
        return False


class Notification:
    """Notification class for managing system notifications"""

    def __init__(self, notification_id: int, message: str, recipient_id: int):
        self.id = notification_id
        self.message = message
        self.recipient_id = recipient_id
        self.created_at = datetime.now().isoformat()
        self.is_read = False
        self.priority = "normal"

    def send(self) -> bool:
        """Send notification"""
        logging.info(f"Notification {self.id} sent to user {self.recipient_id}")
        return True

    def mark_as_read(self) -> None:
        """Mark notification as read"""
        self.is_read = True