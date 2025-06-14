from datetime import datetime, timedelta
from typing import Optional
from models.users import User, Student, Teacher, Parent, Admin
from models.entities import Assignment
from managers.data_manager import DataManager
from managers.export_manager import ExportManager


class CLIInterface:
    """Command Line Interface for edu_platform"""

    def __init__(self, data_manager: DataManager, export_manager: ExportManager):
        self.data_manager = data_manager
        self.export_manager = export_manager
        self.current_user: Optional[User] = None

    def display_banner(self):
        """Display application banner"""
        print("-" * 60)
        print(" edu_platform CLI ")
        print("-" * 60)

    def login(self) -> bool:
        """Handle user login"""
        print("\n Login to EduPlatform")
        email = input("Email: ").strip()
        password = input("Password: ").strip()

        user = self.data_manager.authenticate_user(email, password)
        if user:
            self.current_user = user
            print(f"\n{user._full_name} ({user.role})")
            return True
        else:
            print("Invalid credentials!")
            return False

    def register_user(self) -> bool:
        """Register new user (Admin only)"""
        if not self.current_user or self.current_user.role != "Admin":
            print("Only admins can register new users!")
            return False

        print("\nRegister New User")
        full_name = input("Full Name: ").strip()
        email = input("Email: ").strip()
        password = input("Password: ").strip()

        print("Select Role:")
        print("1. Student")
        print("2. Teacher")
        print("3. Parent")
        print("4. Admin")

        role_choice = input("> ").strip()

        user_id = self.data_manager.get_next_id()

        if role_choice == "1":
            grade = input("Grade (e.g., 9-A): ").strip()
            user = Student(user_id, full_name, email, password, grade)
        elif role_choice == "2":
            subjects_input = input("Subjects (comma-separated): ").strip()
            subjects = [s.strip() for s in subjects_input.split(",")]
            user = Teacher(user_id, full_name, email, password, subjects)
        elif role_choice == "3":
            user = Parent(user_id, full_name, email, password)
        elif role_choice == "4":
            user = Admin(user_id, full_name, email, password)
        else:
            print("Invalid role selection!")
            return False

        self.data_manager.add_user(user)
        print(f"User {full_name} registered successfully!")
        return True

    def admin_menu(self):
        """Admin menu interface"""
        while True:
            print("\n" + "-" * 40)
            print("ADMIN PANEL")
            print("-" * 40)
            print("1. Register New User")
            print("2. View All Users")
            print("3. Generate Reports")
            print("4. Export Data (All Formats)")
            print("5. Export to XLSX")
            print("6. Export to CSV")
            print("7. Export to SQL")
            print("8. View Export Log")
            print("9. System Statistics")
            print("0. Logout")

            choice = input("\nSelect option: ").strip()

            if choice == "1":
                self.register_user()
            elif choice == "2":
                self.view_all_users()
            elif choice == "3":
                self.generate_reports()
            elif choice == "4":
                print("Exporting to all formats...")
                if self.export_manager.auto_export_all():
                    print("All exports completed successfully!")
                else:
                    print("Some exports failed. Check logs for details.")
            elif choice == "5":
                filename = input("XLSX filename (default: eduplatform_data.xlsx): ").strip()
                if not filename:
                    filename = "eduplatform_data.xlsx"
                if self.export_manager.export_to_xlsx(filename):
                    print(f"Data exported to {filename}")
                else:
                    print("XLSX export failed!")
            elif choice == "6":
                directory = input("CSV directory (default: csv_exports): ").strip()
                if not directory:
                    directory = "csv_exports"
                if self.export_manager.export_to_csv(directory):
                    print(f"Data exported to {directory}/")
                else:
                    print("CSV export failed!")
            elif choice == "7":
                filename = input("SQL filename (default: eduplatform_schema.sql): ").strip()
                if not filename:
                    filename = "eduplatform_schema.sql"
                if self.export_manager.export_to_sql(filename):
                    print(f"SQL schema exported to {filename}")
                else:
                    print("SQL export failed!")
            elif choice == "8":
                self.view_export_log()
            elif choice == "9":
                self.show_system_statistics()
            elif choice == "0":
                break
            else:
                print("Invalid option!")

    def teacher_menu(self):
        """Teacher menu interface"""
        teacher = self.current_user

        while True:
            print("\n" + "-" * 40)
            print("TEACHER PANEL")
            print("-" * 40)
            print("1. Create Assignment")
            print("2. View My Assignments")
            print("3. Grade Assignments")
            print("4. View My Profile")
            print("5. View Notifications")
            print("0. Logout")

            choice = input("\nSelect option: ").strip()

            if choice == "1":
                self.create_assignment()
            elif choice == "2":
                self.view_teacher_assignments()
            elif choice == "3":
                self.grade_assignments()
            elif choice == "4":
                self.view_profile()
            elif choice == "5":
                self.view_notifications()
            elif choice == "0":
                break
            else:
                print("Invalid option!")

    def student_menu(self):
        """Student menu interface"""
        while True:
            print("\n" + "-" * 40)
            print("STUDENT PANEL")
            print("-" * 40)
            print("1. View My Grades")
            print("2. View Assignments")
            print("3. Submit Assignment")
            print("4. Calculate Average Grade")
            print("5. View My Profile")
            print("6. View Notifications")
            print("0. Logout")

            choice = input("\nSelect option: ").strip()

            if choice == "1":
                self.view_student_grades()
            elif choice == "2":
                self.view_student_assignments()
            elif choice == "3":
                self.submit_assignment()
            elif choice == "4":
                self.calculate_student_average()
            elif choice == "5":
                self.view_profile()
            elif choice == "6":
                self.view_notifications()
            elif choice == "0":
                break
            else:
                print("Invalid option!")

    def parent_menu(self):
        """Parent menu interface"""
        while True:
            print("\n" + "-" * 40)
            print("PARENT PANEL")
            print("-" * 40)
            print("1. View Children")
            print("2. View Child Grades")
            print("3. View Child Assignments")
            print("4. View My Profile")
            print("5. View Notifications")
            print("0. Logout")

            choice = input("\nSelect option: ").strip()

            if choice == "1":
                self.view_children()
            elif choice == "2":
                self.view_child_grades()
            elif choice == "3":
                self.view_child_assignments()
            elif choice == "4":
                self.view_profile()
            elif choice == "5":
                self.view_notifications()
            elif choice == "0":
                break
            else:
                print("Invalid option!")

    def create_assignment(self):
        """Create new assignment (Teacher)"""
        if not isinstance(self.current_user, Teacher):
            print("Only teachers can create assignments!")
            return

        print("\n Create New Assignment")
        title = input("Assignment Title: ").strip()
        description = input("Description: ").strip()
        subject = input("Subject: ").strip()
        class_id = input("Class ID: ").strip()
        deadline = input("Deadline (YYYY-MM-DD HH:MM): ").strip()

        print("Difficulty Level:")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")

        diff_choice = input("Select difficulty: ").strip()
        difficulty_map = {"1": "easy", "2": "medium", "3": "hard"}
        difficulty = difficulty_map.get(diff_choice, "medium")

        # Add ISO format to deadline
        try:
            deadline_dt = datetime.strptime(deadline, "%Y-%m-%d %H:%M")
            deadline_iso = deadline_dt.isoformat()
        except ValueError:
            print("Invalid date format!")
            return

        assignment_id = self.current_user.create_assignment(
            title, description, deadline_iso, subject, class_id, difficulty
        )

        # Store in data manager
        assignment = self.current_user.assignments[assignment_id]
        self.data_manager.assignments[assignment_id] = assignment

        print(f"Assignment '{title}' created successfully! (ID: {assignment_id})")

    def view_teacher_assignments(self):
        """View teacher's assignments"""
        if not isinstance(self.current_user, Teacher):
            return

        print("\n My Assignments")
        print("-" * 50)

        if not self.current_user.assignments:
            print("No assignments created yet.")
            return

        for assignment in self.current_user.assignments.values():
            status = assignment.get_status()
            print(f"ID: {status['id']}")
            print(f"Title: {status['title']}")
            print(f"Submissions: {status['submissions']}")
            print(f"Graded: {status['graded']}")
            print(f"Deadline: {status['deadline']}")
            print("-" * 30)

    def grade_assignments(self):
        """Grade student assignments"""
        if not isinstance(self.current_user, Teacher):
            return

        if not self.current_user.assignments:
            print("No assignments to grade.")
            return

        print("\n Grade Assignments")
        print("Available assignments:")

        for assignment in self.current_user.assignments.values():
            print(f"ID: {assignment.id} - {assignment.title}")

        try:
            assignment_id = int(input("Enter assignment ID to grade: "))
            student_id = int(input("Enter student ID: "))
            grade = int(input("Enter grade (1-5): "))
            comment = input("Comment (optional): ").strip()

            if self.current_user.grade_assignment(assignment_id, student_id, grade):
                print(" Grade assigned successfully!")
            else:
                print(" Failed to assign grade!")

        except ValueError:
            print(" Invalid input!")

    def view_student_grades(self):
        """View student grades"""
        if not isinstance(self.current_user, Student):
            return

        print("\n My Grades")
        print("-" * 30)

        grades = self.current_user.view_grades()
        if not grades:
            print("No grades recorded yet.")
            return

        for subject, grade_list in grades.items():
            if grade_list:
                avg = sum(grade_list) / len(grade_list)
                print(f"{subject}: {grade_list} (Average: {avg:.2f})")
            else:
                print(f"{subject}: No grades yet")

    def submit_assignment(self):
        """Submit assignment (Student)"""
        if not isinstance(self.current_user, Student):
            return

        print("\n Submit Assignment")

        # Show available assignments
        if not self.data_manager.assignments:
            print("No assignments available.")
            return

        print("Available assignments:")
        for assignment in self.data_manager.assignments.values():
            print(f"ID: {assignment.id} - {assignment.title} (Due: {assignment.deadline})")

        try:
            assignment_id = int(input("Enter assignment ID: "))
            content = input("Enter your assignment content: ").strip()

            if self.current_user.submit_assignment(assignment_id, content):
                # Also add to assignment submissions
                if assignment_id in self.data_manager.assignments:
                    assignment = self.data_manager.assignments[assignment_id]
                    assignment.add_submission(self.current_user._id, content)
                print(" Assignment submitted successfully!")
            else:
                print(" Failed to submit assignment!")

        except ValueError:
            print(" Invalid input!")

    def calculate_student_average(self):
        """Calculate and display student's average grade"""
        if not isinstance(self.current_user, Student):
            return

        overall_avg = self.current_user.calculate_average_grade()
        print(f"\n Your overall average grade: {overall_avg:.2f}")

        print("\nSubject averages:")
        for subject in self.current_user.grades.keys():
            subject_avg = self.current_user.calculate_average_grade(subject)
            print(f"  {subject}: {subject_avg:.2f}")

    def view_all_users(self):
        """View all users (Admin only)"""
        if self.current_user.role != "Admin":
            return

        print("\n All Users")
        print("-" * 80)
        print(f"{'ID':<5} {'Name':<20} {'Email':<25} {'Role':<10} {'Created':<20}")
        print("-" * 80)

        for user in self.data_manager.users.values():
            profile = user.get_profile()
            print(
                f"{profile['id']:<5} {profile['full_name']:<20} {profile['email']:<25} {profile['role']:<10} {profile['created_at'][:10]:<20}")

    def generate_reports(self):
        """Generate system reports (Admin only)"""
        if self.current_user.role != "Admin":
            return

        print("\n System Reports")
        print("1. User Statistics")
        print("2. Assignment Reports")
        print("3. Grade Analysis")

        choice = input("Select report type: ").strip()

        if choice == "1":
            self.show_user_statistics()
        elif choice == "2":
            self.show_assignment_reports()
        elif choice == "3":
            self.show_grade_analysis()

    def show_user_statistics(self):
        """Show user statistics"""
        total_users = len(self.data_manager.users)
        students = len(self.data_manager.students)
        teachers = len(self.data_manager.teachers)
        parents = len(self.data_manager.parents)
        admins = len(self.data_manager.admins)

        print(f"\n User Statistics")
        print(f"Total Users: {total_users}")
        print(f"Students: {students}")
        print(f"Teachers: {teachers}")
        print(f"Parents: {parents}")
        print(f"Admins: {admins}")

    def show_assignment_reports(self):
        """Show assignment reports"""
        total_assignments = len(self.data_manager.assignments)
        total_submissions = sum(len(a.submissions) for a in self.data_manager.assignments.values())
        total_graded = sum(len(a.grades) for a in self.data_manager.assignments.values())

        print(f"\n Assignment Reports")
        print(f"Total Assignments: {total_assignments}")
        print(f"Total Submissions: {total_submissions}")
        print(f"Total Graded: {total_graded}")

        if total_assignments > 0:
            completion_rate = (total_submissions / total_assignments) * 100
            grading_rate = (total_graded / total_submissions) * 100 if total_submissions > 0 else 0
            print(f"Completion Rate: {completion_rate:.1f}%")
            print(f"Grading Rate: {grading_rate:.1f}%")

    def show_grade_analysis(self):
        """Show grade analysis"""
        all_grades = []
        for student in self.data_manager.students.values():
            for grade_list in student.grades.values():
                all_grades.extend(grade_list)

        if all_grades:
            avg_grade = sum(all_grades) / len(all_grades)
            max_grade = max(all_grades)
            min_grade = min(all_grades)

            print(f"\n Grade Analysis")
            print(f"Total Grades: {len(all_grades)}")
            print(f"Average Grade: {avg_grade:.2f}")
            print(f"Highest Grade: {max_grade}")
            print(f"Lowest Grade: {min_grade}")
        else:
            print("No grades recorded yet.")

    def show_system_statistics(self):
        """Show comprehensive system statistics"""
        print(f"\n📈 System Statistics")
        print("=" * 40)

        self.show_user_statistics()
        self.show_assignment_reports()
        self.show_grade_analysis()

        # Additional statistics
        total_notifications = sum(len(user._notifications) for user in self.data_manager.users.values())
        print(f"\nTotal Notifications: {total_notifications}")

    def view_export_log(self):
        """View export operation log"""
        print("\n Export Log")
        print("-" * 60)

        if not self.export_manager.export_log:
            print("No export operations logged yet.")
            return

        for log_entry in self.export_manager.export_log[-10:]:  # Show last 10 entries
            status = "✅" if log_entry['success'] else "❌"
            print(f"{status} {log_entry['timestamp'][:19]} - {log_entry['format']} - {log_entry['filename']}")

    def view_profile(self):
        """View current user profile"""
        profile = self.current_user.get_profile()
        print(f"\n Your Profile")
        print("-" * 30)
        print(f"ID: {profile['id']}")
        print(f"Name: {profile['full_name']}")
        print(f"Email: {profile['email']}")
        print(f"Role: {profile['role']}")
        print(f"Joined: {profile['created_at'][:10]}")
        print(f"Phone: {profile['phone'] or 'Not set'}")
        print(f"Address: {profile['address'] or 'Not set'}")

    def view_notifications(self):
        """View user notifications"""
        notifications = self.current_user.view_notifications()

        print(f"\n Your Notifications ({len(notifications)})")
        print("-" * 50)

        if not notifications:
            print("No notifications.")
            return

        for notif in notifications[-10:]:  # Show last 10
            status = "🔴" if notif['priority'] == 'high' else "🔵"
            read_status = "📖" if notif['is_read'] else "📫"
            print(f"{status} {read_status} {notif['message']}")
            print(f"   {notif['created_at'][:19]}")
            print()

    def view_children(self):
        """View parent's children"""
        if not isinstance(self.current_user, Parent):
            return

        print(f"\n Your Children")
        print("-" * 30)

        if not self.current_user.children:
            print("No children registered.")
            return

        for child_id in self.current_user.children:
            if child_id in self.data_manager.students:
                student = self.data_manager.students[child_id]
                print(f"ID: {student._id}")
                print(f"Name: {student._full_name}")
                print(f"Grade: {student.grade}")
                print(f"Average: {student.calculate_average_grade():.2f}")
                print("-" * 20)

    def view_child_grades(self):
        """View child's grades (Parent)"""
        if not isinstance(self.current_user, Parent):
            return

        if not self.current_user.children:
            print("No children registered.")
            return

        print("Select child:")
        for i, child_id in enumerate(self.current_user.children, 1):
            if child_id in self.data_manager.students:
                student = self.data_manager.students[child_id]
                print(f"{i}. {student._full_name}")

        try:
            choice = int(input("Enter choice: ")) - 1
            if 0 <= choice < len(self.current_user.children):
                child_id = self.current_user.children[choice]
                student = self.data_manager.students[child_id]

                print(f"\n {student._full_name}'s Grades")
                print("-" * 30)

                for subject, grades in student.grades.items():
                    if grades:
                        avg = sum(grades) / len(grades)
                        print(f"{subject}: {grades} (Average: {avg:.2f})")
                    else:
                        print(f"{subject}: No grades yet")
        except (ValueError, IndexError):
            print(" Invalid selection!")

    def view_child_assignments(self):
        """View child's assignments (Parent)"""
        if not isinstance(self.current_user, Parent):
            return

        # Similar implementation to view_child_grades
        print("Child assignment viewing feature - Implementation needed")

    def view_student_assignments(self):
        """View assignments for student"""
        if not isinstance(self.current_user, Student):
            return

        print(f"\n Available Assignments")
        print("-" * 50)

        if not self.data_manager.assignments:
            print("No assignments available.")
            return

        for assignment in self.data_manager.assignments.values():
            status = " Submitted" if assignment.id in self.current_user.assignments else " Not Submitted"
            print(f"ID: {assignment.id}")
            print(f"Title: {assignment.title}")
            print(f"Subject: {assignment.subject}")
            print(f"Due: {assignment.deadline}")
            print(f"Status: {status}")
            print("-" * 30)

    def run(self):
        """Main application loop"""
        self.display_banner()

        # Create sample data for demonstration
        self.create_sample_data()

        while True:
            if not self.current_user:
                print("\n Authentication Required")
                print("1. Login")
                print("2. Exit")

                choice = input("\nSelect option: ").strip()

                if choice == "1":
                    if self.login():
                        continue
                elif choice == "2":
                    print(" Goodbye!")
                    break
                else:
                    print(" Invalid option!")
            else:
                # Route to appropriate menu based on user role
                if self.current_user.role == "Admin":
                    self.admin_menu()
                elif self.current_user.role == "Teacher":
                    self.teacher_menu()
                elif self.current_user.role == "Student":
                    self.student_menu()
                elif self.current_user.role == "Parent":
                    self.parent_menu()

                # Logout
                self.current_user = None
                print(" Logged out successfully!")

    def create_sample_data(self):
        """Create sample data for demonstration"""
        # Create sample admin
        admin = Admin(1, "System Admin", "admin@edu.com", "admin123")
        self.data_manager.add_user(admin)

        # Create sample teacher
        teacher = Teacher(2, "John Adam", "john@edu.com", "teacher123", ["Mathematics", "Physics"])
        teacher.classes = ["9-A", "10-B"]
        teacher.workload = 20
        self.data_manager.add_user(teacher)

        # Create sample student
        student = Student(3, "Alice Adam", "alice@edu.com", "student123", "9-A")
        student.subjects = {"Mathematics": 2, "Physics": 2}
        student.grades = {"Mathematics": [4, 5, 4], "Physics": [5, 4, 5]}
        self.data_manager.add_user(student)

        # Create sample parent
        parent = Parent(4, "Bob Adam", "bob@edu.com", "parent123")
        parent.children = [3]  # Alice is Bob's child
        self.data_manager.add_user(parent)

        # Create sample assignment
        assignment = Assignment(
            1, "Python task", "Solve the given task",
            (datetime.now() + timedelta(days=7)).isoformat(),
            "CS", 2, "9-A", "medium"
        )
        self.data_manager.assignments[1] = assignment
        teacher.assignments[1] = assignment

        print("Sample login credentials:")
        print("Admin: admin@edu.com / admin123")
        print("Teacher: john@edu.com / teacher123")
        print("Student: alice@edu.com / student123")
        print("Parent: bob@edu.com / parent123")