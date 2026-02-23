CREATE DATABASE attendance_db;
USE attendance_db;

-- STUDENT TABLE
CREATE TABLE Student (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    roll_no VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    department VARCHAR(50) NOT NULL
);

-- FACULTY TABLE
CREATE TABLE Faculty (
    faculty_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    department VARCHAR(50) NOT NULL
);

-- SUBJECT TABLE
CREATE TABLE Subject (
    subject_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_name VARCHAR(50) NOT NULL,
    faculty_id INT,
    FOREIGN KEY (faculty_id)
    REFERENCES Faculty(faculty_id)
);

-- ENROLLMENT TABLE
CREATE TABLE Enrollment (
    enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    subject_id INT NOT NULL,
    FOREIGN KEY (student_id)
    REFERENCES Student(student_id),
    FOREIGN KEY (subject_id)
    REFERENCES Subject(subject_id),
    UNIQUE(student_id, subject_id)
);

-- ATTENDANCE TABLE
CREATE TABLE Attendance (
    attendance_id INT AUTO_INCREMENT PRIMARY KEY,
    enrollment_id INT NOT NULL,
    date DATE NOT NULL,
    status VARCHAR(10) NOT NULL,
    FOREIGN KEY (enrollment_id)
    REFERENCES Enrollment(enrollment_id),
    CHECK (status IN ('Present','Absent')),
    UNIQUE(enrollment_id, date)
);

-- INSERT DATA
INSERT INTO Student (roll_no, name, email, department)
VALUES
('IT101','Rahul Sharma','rahul@email.com','IT'),
('IT102','Priya Singh','priya@email.com','IT');

INSERT INTO Faculty (name, email, department)
VALUES
('Dr. Mehta','mehta@email.com','IT');

INSERT INTO Subject (subject_name, faculty_id)
VALUES
('Database Management',1);

INSERT INTO Enrollment (student_id, subject_id)
VALUES
(1,1),
(2,1);

INSERT INTO Attendance (enrollment_id, date, status)
VALUES
(1,'2026-02-17','Present'),
(2,'2026-02-17','Absent');

-- TRANSACTION
START TRANSACTION;

INSERT INTO Attendance (enrollment_id,date,status)
VALUES (1,'2026-02-18','Present');

INSERT INTO Attendance (enrollment_id,date,status)
VALUES (2,'2026-02-18','Present');

COMMIT;

-- STORED PROCEDURE
DELIMITER //

CREATE PROCEDURE MarkAttendance(
IN enroll_id INT,
IN att_date DATE,
IN att_status VARCHAR(10)
)
BEGIN
INSERT INTO Attendance(enrollment_id,date,status)
VALUES(enroll_id,att_date,att_status);
END //

DELIMITER ;

CALL MarkAttendance(1,'2026-02-19','Present');

-- TRIGGER
DELIMITER //

CREATE TRIGGER prevent_duplicate_attendance
BEFORE INSERT ON Attendance
FOR EACH ROW
BEGIN
IF EXISTS(
SELECT 1 FROM Attendance
WHERE enrollment_id=NEW.enrollment_id
AND date=NEW.date
)
THEN
SIGNAL SQLSTATE '45000'
SET MESSAGE_TEXT='Duplicate attendance not allowed';
END IF;
END //

DELIMITER ;

-- INDEX
CREATE INDEX idx_roll_no ON Student(roll_no);

-- USER SECURITY
CREATE USER 'faculty_user'@'localhost'
IDENTIFIED BY 'faculty123';

GRANT SELECT, INSERT ON attendance_db.Attendance
TO 'faculty_user'@'localhost';

-- VIEW (FINAL REPORT)
CREATE VIEW Attendance_Report AS
SELECT
s.student_id,
s.roll_no,
s.name AS student_name,
s.department,
f.name AS faculty_name,
sub.subject_name,
a.date,
a.status
FROM Attendance a
JOIN Enrollment e ON a.enrollment_id=e.enrollment_id
JOIN Student s ON e.student_id=s.student_id
JOIN Subject sub ON e.subject_id=sub.subject_id
JOIN Faculty f ON sub.faculty_id=f.faculty_id;

-- FINAL OUTPUT
SELECT * FROM Attendance_Report;















