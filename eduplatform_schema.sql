-- EduPlatform Database Schema for SQL Server
-- Generated on: 2025-06-14T17:28:57.373198

-- Create Users table
CREATE TABLE Users
                           (
                               ID           INT PRIMARY KEY,
                               FullName     NVARCHAR(255) NOT NULL,
                               Email        NVARCHAR(255) UNIQUE NOT NULL,
                               PasswordHash NVARCHAR(255) NOT NULL,
                               Role         NVARCHAR(50) NOT NULL,
                               CreatedAt    DATETIME2 NOT NULL,
                               Phone        NVARCHAR(20),
                               Address      NVARCHAR(500)
                           );

-- Create Students table
CREATE TABLE Students
                           (
                               UserID       INT PRIMARY KEY,
                               Grade        NVARCHAR(10) NOT NULL,
                               Subjects     NVARCHAR(MAX),
                               AverageGrade FLOAT,
                               FOREIGN KEY (UserID) REFERENCES Users (ID)
                           );

-- Create Teachers table
CREATE TABLE Teachers
                           (
                               UserID   INT PRIMARY KEY,
                               Subjects NVARCHAR(MAX),
                               Classes  NVARCHAR(MAX),
                               Workload INT DEFAULT 0,
                               FOREIGN KEY (UserID) REFERENCES Users (ID)
                           );

-- Create Assignments table
CREATE TABLE Assignments
                           (
                               ID              INT PRIMARY KEY,
                               Title           NVARCHAR(255) NOT NULL,
                               Description     NVARCHAR(MAX),
                               Subject         NVARCHAR(100) NOT NULL,
                               TeacherID       INT       NOT NULL,
                               ClassID         NVARCHAR(50) NOT NULL,
                               Deadline        DATETIME2 NOT NULL,
                               Difficulty      NVARCHAR(20) DEFAULT 'medium',
                               SubmissionCount INT DEFAULT 0,
                               GradeCount      INT DEFAULT 0,
                               FOREIGN KEY (TeacherID) REFERENCES Users (ID)
                           );

-- Insert Users data
INSERT INTO Users VALUES (1, N'System Admin', 'admin@edu.com', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'Admin', '2025-06-14T17:26:27.561289', '', N'');
INSERT INTO Users VALUES (2, N'John Adam', 'john@edu.com', 'cde383eee8ee7a4400adf7a15f716f179a2eb97646b37e089eb8d6d04e663416', 'Teacher', '2025-06-14T17:26:27.561304', '', N'');
INSERT INTO Users VALUES (3, N'Alice Adam', 'alice@edu.com', '703b0a3d6ad75b649a28adde7d83c6251da457549263bc7ff45ec709b0a8448b', 'Student', '2025-06-14T17:26:27.561309', '', N'');
INSERT INTO Users VALUES (4, N'Bob Adam', 'bob@edu.com', '82e3edf5f5f3a46b5f94579b61817fd9a1f356adcef5ee22da3b96ef775c4860', 'Parent', '2025-06-14T17:26:27.561313', '', N'');

-- Insert Students data
INSERT INTO Students VALUES (3, '9-A', N'Mathematics, Physics', 4.5);

-- Insert Teachers data
INSERT INTO Teachers VALUES (2, N'Mathematics, Physics', N'9-A, 10-B', 20);

-- Insert Assignments data
INSERT INTO Assignments VALUES (1, N'Python task', N'Solve the given task', 'CS', 2, '9-A', '2025-06-21T17:26:27.561316', 'medium', 0, 0);
