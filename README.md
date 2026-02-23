📊 Attendance Management System (Python + MySQL)
📌 Project Overview

The Attendance Management System is a desktop-based application developed using Python (Tkinter GUI) and MySQL database.
This system is designed to simplify the process of managing student attendance in educational institutions by providing an easy-to-use graphical interface and a structured backend database.

The project eliminates manual attendance registers and provides accurate, secure, and efficient attendance management.

🎯 Objectives

To automate the attendance process

To reduce paperwork and human errors

To store attendance data securely in a database

To provide quick viewing and deletion of attendance records

To create a user-friendly GUI for teachers/admins

🛠️ Technologies Used
Component	Technology
Programming Language	Python 3.11
GUI Framework	Tkinter
Database	MySQL
Connector	mysql-connector-python
IDE	VS Code / PyCharm
OS	Windows
📂 Features
✅ Student Management

Add student details (Enrollment Number, Name)

Store data securely in MySQL

✅ Subject Management

Add subjects dynamically

Maintain subject list for attendance mapping

✅ Attendance Management

Mark attendance as Present / Absent

Automatically records attendance date

Prevents incorrect data entry

✅ View Attendance

Displays complete attendance records

Shows student name, enrollment, subject, date, and status

✅ Delete Attendance

Delete incorrect or unwanted attendance records

Updates database instantly

🗄️ Database Structure
📘 Students Table

student_id (Primary Key)

enrollment_no

name

📘 Subjects Table

subject_id (Primary Key)

subject_name

📘 Attendance Table

attendance_id (Primary Key)

student_id (Foreign Key)

subject_id (Foreign Key)

attendance_date

status

🖥️ GUI Modules

Add Student Window

Add Subject Window

Mark Attendance Window

View Attendance Window

Delete Attendance Option

⚙️ Installation & Setup
1️⃣ Prerequisites

Python 3.10 or above

MySQL Server

mysql-connector-python library

Install connector:

pip install mysql-connector-python
2️⃣ Database Setup

Run the following command in MySQL:

CREATE DATABASE AttendanceManagementSystem;
3️⃣ Run the Project
python attendance_gui.py
📸 Output Screens

Student Entry Screen

Subject Entry Screen

Mark Attendance Screen

View Attendance Table

Delete Attendance Option

🔐 Error Handling & Security

Uses ID-mapping technique to avoid parsing errors

Prevents empty field submission

Ensures referential integrity using foreign keys

📈 Future Enhancements

Login authentication system

Attendance percentage calculation

Export attendance to Excel/PDF

Role-based access (Admin / Teacher)

Cloud database integration

🎓 Academic Relevance

Suitable for OS + DBMS Mini Project

Covers concepts of:

GUI Programming

Database Connectivity

SQL Queries

CRUD Operations

Exception Handling

👩‍💻 Developed By

Name: Janhavi Amberkar
Course: SY IT
Project Type: Academic Mini Project

📜 License

This project is created for educational purposes only.
