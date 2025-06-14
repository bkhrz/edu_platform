# EduPlatform - Educational Management System

## 📋 Project Overview

**Project Name:** EduPlatform  
**Objective:** Develop an educational platform similar to Kundalik.com using Python with Object-Oriented Programming (OOP) principles. The system operates without a traditional backend database, storing all data in-memory using classes, lists, and dictionaries.

**Technology Stack:**
- Python 3.x
- OOP Principles (Encapsulation, Inheritance, Polymorphism, Abstraction)
- In-memory data storage (no database required)
- Export capabilities: XLSX, CSV, and SQL Server Management Studio (SSMS)

**User Roles:**
- **Admin:** System management, user creation/deletion
- **Teacher:** Assignment creation, grading, schedule management
- **Student:** Assignment submission, grade viewing
- **Parent:** Child progress monitoring

## 🏗️ System Architecture

### Core Classes and Models

#### AbstractRole (Abstract Base Class)
Base class for all user roles with common functionality.

**Attributes:**
- `_id`: Unique identifier (int)
- `_full_name`: Full name (str)
- `_email`: Email address (str)
- `_password_hash`: Hashed password (str)
- `_created_at`: Registration date (str, ISO format)

**Abstract Methods:**
- `get_profile()`: Return user profile information
- `update_profile()`: Update user profile

#### User (Inherits from AbstractRole)
Base user class with common user functionality.

**Additional Attributes:**
- `role`: User role (enum: Admin, Teacher, Student, Parent)
- `_notifications`: List of notifications

**Methods:**
- `add_notification(message)`: Add notification
- `view_notifications()`: View all notifications
- `delete_notification(id)`: Delete specific notification

#### Student (Inherits from User)
Student-specific functionality and data management.

**Attributes:**
- `grade`: Class/grade level (e.g., "9-A")
- `subjects`: Enrolled subjects (dict: {subject_name: teacher_id})
- `assignments`: Assignment status (dict: {assignment_id: status})
- `grades`: Academic grades (dict: {subject: [grade1, grade2, ...]})

**Methods:**
- `submit_assignment(assignment_id, content)`: Submit assignment
- `view_grades(subject=None)`: View grades (filterable by subject)
- `calculate_average_grade()`: Calculate average grade

#### Teacher (Inherits from User)
Teacher-specific functionality for course management.

**Attributes:**
- `subjects`: Teaching subjects (list)
- `classes`: Teaching classes (list)
- `assignments`: Created assignments (dict: {assignment_id: Assignment})

**Methods:**
- `create_assignment(title, description, deadline, subject, class_id)`: Create new assignment
- `grade_assignment(assignment_id, student_id, grade)`: Grade student assignment
- `view_student_progress(student_id)`: View student progress

#### Parent (Inherits from User)
Parent-specific functionality for child monitoring.

**Attributes:**
- `children`: List of child student IDs

**Methods:**
- `view_child_grades(child_id)`: View child's grades
- `view_child_assignments(child_id)`: View child's assignments
- `receive_child_notification(child_id)`: Receive child-related notifications

#### Admin (Inherits from User)
Administrator functionality for system management.

**Attributes:**
- `permissions`: List of admin permissions

**Methods:**
- `add_user(user)`: Add new user to system
- `remove_user(user_id)`: Remove user from system
- `generate_report()`: Generate system reports

### Supporting Classes

#### Assignment
Assignment management and tracking.

**Attributes:**
- `id`: Assignment ID (int)
- `title`: Assignment title (str)
- `description`: Assignment description (str)
- `deadline`: Submission deadline (str, ISO format)
- `subject`: Subject name (str)
- `teacher_id`: Teacher ID (int)
- `class_id`: Class ID (str)
- `submissions`: Student submissions (dict: {student_id: content})
- `grades`: Assignment grades (dict: {student_id: grade})

**Methods:**
- `add_submission(student_id, content)`: Add student submission
- `set_grade(student_id, grade)`: Set grade for submission
- `get_status()`: Get assignment status

#### Grade
Grade management and tracking.

**Attributes:**
- `id`: Grade ID (int)
- `student_id`: Student ID (int)
- `subject`: Subject name (str)
- `value`: Grade value (int, 1-5)
- `date`: Grade date (str, ISO format)
- `teacher_id`: Teacher ID (int)

**Methods:**
- `update_grade(value)`: Update grade value
- `get_grade_info()`: Get grade information

#### Schedule
Class schedule management.

**Attributes:**
- `id`: Schedule ID (int)
- `class_id`: Class ID (str)
- `day`: Day of week (str)
- `lessons`: Daily lessons (dict: {time: {subject, teacher_id}})

**Methods:**
- `add_lesson(time, subject, teacher_id)`: Add lesson to schedule
- `view_schedule()`: View complete schedule
- `remove_lesson(time)`: Remove lesson from schedule

#### Notification
Notification system management.

**Attributes:**
- `id`: Notification ID (int)
- `message`: Notification message (str)
- `recipient_id`: Recipient ID (int)
- `created_at`: Creation date (str)

**Methods:**
- `send()`: Send notification
- `mark_as_read()`: Mark notification as read

## 🚀 Key Features

### User Management
- User registration with password hashing
- Role-based access control
- Profile management with additional information (phone, address)

### Assignment System
- Assignment difficulty levels (easy, medium, hard)
- Group-based assignment distribution
- File format and size validation for submissions
- Late submission tracking

### Grading System
- Statistical analysis (average, highest, lowest grades)
- Grade comments and feedback
- Grade history tracking
- Performance analytics

### Schedule Management
- Conflict detection (preventing double-booking)
- Weekly and monthly schedule views
- Teacher availability tracking
- Automatic schedule optimization

### Notification System
- Automatic notifications (assignment deadlines, grade updates)
- Notification filtering (unread, important)
- Parent-specific notifications (low grades, attendance)
- Priority-based notification delivery

### Reporting System
- Student performance graphs by subject
- Teacher workload analysis
- Class-wide statistics
- Export capabilities for various formats

## 💾 Data Storage Structure

### In-Memory Data Tables

#### Users Table
```
id, full_name, email, password_hash, role, created_at, phone, address
```

#### Students Table
```
user_id, grade, subjects (dict), assignments (dict), grades (dict)
```

#### Teachers Table
```
user_id, subjects, classes, workload (teaching hours)
```

#### Parents Table
```
user_id, children (list of Student IDs), notification_preferences (dict)
```

#### Assignments Table
```
id, title, description, deadline, subject, teacher_id, class_id, difficulty, submissions, grades
```

#### Grades Table
```
id, student_id, subject, value, date, teacher_id, comment
```

#### Schedules Table
```
id, class_id, day, lessons (dict)
```

#### Notifications Table
```
id, message, recipient_id, created_at, is_read, priority
```

## 📊 Data Export Capabilities

### Export Formats

#### XLSX Export
- `export_to_xlsx()`: Export data to Excel format
- Each table gets its own worksheet
- Formatted headers and data validation

#### CSV Export
- `export_to_csv()`: Export data to CSV format
- Separate file for each data table
- UTF-8 encoding support

#### SQL Server Export
- `export_to_sql()`: Generate SQL INSERT statements
- Compatible with SQL Server Management Studio (SSMS)
- Includes CREATE TABLE statements with constraints

### Export Features
- **Automatic Export:** Real-time data export on creation/modification
- **Incremental Export:** Export only new or modified data
- **Data Validation:** Pre-export data integrity checks
- **SQL Constraints:** PRIMARY KEY, FOREIGN KEY, and CHECK constraints
- **Export Logging:** Complete audit trail of export operations

## 🔧 Advanced Features

### Assignment Monitoring
- Automatic late submission flagging
- Deadline reminder notifications
- Assignment completion tracking

### Statistical Analysis
- Subject-wise performance calculation
- Top performer identification
- Trend analysis and reporting

### Schedule Optimization
- Teacher availability conflict resolution
- Automatic schedule balancing
- Resource allocation optimization

### Security Features
- Password hashing using hashlib
- User authentication system
- Role-based permission management

### Complex Task Management
- **Submission Constraints:** Format and length validation
- **Grade Analysis:** Comprehensive statistical calculations
- **Schedule Optimization:** Conflict prevention algorithms
- **Notification Prioritization:** Important alerts first
- **Report Generation:** CSV export capabilities for admins

## 🛠️ Installation and Setup

1. **Prerequisites:**
   ```bash
   Python 3.8+
   Required libraries: hashlib, datetime, json, csv, openpyxl
   ```

2. **Installation:**
   ```bash
   git clone <repository-url>
   cd eduplatform
   pip install -r requirements.txt
   ```

3. **Usage:**
   ```python
   from eduplatform import EduPlatform
   
   # Initialize platform
   platform = EduPlatform()
   
   # Create admin user
   admin = platform.create_admin("Admin User", "admin@edu.com", "password")
   
   # Start using the platform
   platform.run()
   ```

## 📈 Future Enhancements

- Web interface integration
- Real database connectivity
- Mobile application support
- Advanced analytics dashboard
- Multi-language support
- Cloud storage integration


## 📞 Support

For support and questions, please contact:
- Email: behruzqobilov26@gmail.com

---

**Note:** This is an educational project designed to demonstrate OOP principles in Python. For production use, consider implementing proper database connectivity and security measures.
