from models.base import User
from models.entities import Assignment
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging


class Student(User):
    """Student class with academic functionality"""

    def __init__(self, user_id: int, full_name: str, email: str, password: str, grade: str):
        super().__init__(user_id, full_name, email, password, "Student")
        self.grade = grade
        self.subjects: Dict[str, int] = {}  # {subject: teacher_id}
        self.assignments: Dict[int, str] = {}  # {assignment_id: status}
        self.grades: Dict[str, List[int]] = {}  # {subject: [grades]}

    def submit_assignment(self, assignment_id: int, content: str) -> bool:
        """Submit assignment"""
        if len(content) > 500:
            print("❌ Assignment content too long (max 500 characters)")
            return False

        self.assignments[assignment_id] = "submitted"
        logging.info(f"Student {self._id} submitted assignment {assignment_id}")
        return True

    def view_grades(self, subject: Optional[str] = None) -> Dict[str, List[int]]:
        """View grades, optionally filtered by subject"""
        if subject:
            return {subject: self.grades.get(subject, [])}
        return self.grades

    def calculate_average_grade(self, subject: Optional[str] = None) -> float:
        """Calculate average grade"""
        if subject:
            grades = self.grades.get(subject, [])
            return sum(grades) / len(grades) if grades else 0.0

        all_grades = []
        for subject_grades in self.grades.values():
            all_grades.extend(subject_grades)

        return sum(all_grades) / len(all_grades) if all_grades else 0.0


class Teacher(User):
    """Teacher class with teaching functionality"""

    def __init__(self, user_id: int, full_name: str, email: str, password: str, subjects: List[str]):
        super().__init__(user_id, full_name, email, password, "Teacher")
        self.subjects = subjects
        self.classes: List[str] = []
        self.assignments: Dict[int, 'Assignment'] = {}
        self.workload = 0  # Teaching hours per week

    def create_assignment(self, title: str, description: str, deadline: str,
                          subject: str, class_id: str, difficulty: str = "medium") -> int:
        """Create new assignment"""
        assignment_id = len(self.assignments) + 1
        assignment = Assignment(
            assignment_id, title, description, deadline,
            subject, self._id, class_id, difficulty
        )
        self.assignments[assignment_id] = assignment
        logging.info(f"Teacher {self._id} created assignment: {title}")
        return assignment_id

    def grade_assignment(self, assignment_id: int, student_id: int, grade: int) -> bool:
        """Grade student assignment"""
        if assignment_id in self.assignments:
            assignment = self.assignments[assignment_id]
            assignment.set_grade(student_id, grade)
            logging.info(f"Teacher {self._id} graded assignment {assignment_id} for student {student_id}: {grade}")
            return True
        return False

    def view_student_progress(self, student_id: int) -> Dict[str, Any]:
        """View specific student's progress"""
        # This would be implemented with access to the data manager
        return {"student_id": student_id, "progress": "Implementation needed"}


class Parent(User):
    """Parent class with child monitoring functionality"""

    def __init__(self, user_id: int, full_name: str, email: str, password: str):
        super().__init__(user_id, full_name, email, password, "Parent")
        self.children: List[int] = []  # List of student IDs
        self.notification_preferences = {
            'grade_alerts': True,
            'assignment_due': True,
            'attendance': True
        }

    def view_child_grades(self, child_id: int) -> Dict[str, Any]:
        """View child's grades"""
        # Implementation would require access to student data
        return {"child_id": child_id, "grades": "Implementation needed"}

    def view_child_assignments(self, child_id: int) -> Dict[str, Any]:
        """View child's assignments"""
        return {"child_id": child_id, "assignments": "Implementation needed"}

    def receive_child_notification(self, child_id: int, message: str) -> None:
        """Receive notification about child"""
        self.add_notification(f"Child {child_id}: {message}", priority="high")


class Admin(User):
    """Admin class with system management functionality"""

    def __init__(self, user_id: int, full_name: str, email: str, password: str):
        super().__init__(user_id, full_name, email, password, "Admin")
        self.permissions = [
            "manage_users", "view_reports", "system_settings",
            "data_export", "backup_restore"
        ]

    def add_user(self, user_data: Dict[str, Any]) -> bool:
        """Add new user to system"""
        logging.info(f"Admin {self._id} adding new user: {user_data.get('email')}")
        return True

    def remove_user(self, user_id: int) -> bool:
        """Remove user from system"""
        logging.info(f"Admin {self._id} removing user: {user_id}")
        return True

    def generate_report(self, report_type: str) -> Dict[str, Any]:
        """Generate system report"""
        return {
            "report_type": report_type,
            "generated_at": datetime.now().isoformat(),
            "generated_by": self._id
        }