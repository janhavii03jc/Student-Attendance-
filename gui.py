import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# ---------------- DATABASE CONNECTION ----------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="janhavi",
        password="root_456_j",  # CHANGE IF NEEDED
        database="attendance_db"
    )

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Attendance Management System")
root.geometry("1250x700")
root.configure(bg="#f0f2f5")

title = tk.Label(root, text="Attendance Management System",
                 font=("Segoe UI", 22, "bold"),
                 bg="#1f2937", fg="white", pady=12)
title.pack(fill="x")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# ---------------- COMMON TREE FUNCTION ----------------
def create_tree(frame, columns):
    tree = ttk.Treeview(frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.pack(fill="both", expand=True, pady=10)
    return tree

# ======================================================
# ================= STUDENT TAB ========================
# ======================================================
student_tab = tk.Frame(notebook, bg="white")
notebook.add(student_tab, text="Student")

tk.Label(student_tab, text="Roll No").pack()
roll_entry = tk.Entry(student_tab)
roll_entry.pack()

tk.Label(student_tab, text="Name").pack()
name_entry = tk.Entry(student_tab)
name_entry.pack()

tk.Label(student_tab, text="Email").pack()
email_entry = tk.Entry(student_tab)
email_entry.pack()

tk.Label(student_tab, text="Department").pack()
dept_entry = tk.Entry(student_tab)
dept_entry.pack()

def add_student():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO Student(roll_no,name,email,department) VALUES(%s,%s,%s,%s)",
                    (roll_entry.get(), name_entry.get(), email_entry.get(), dept_entry.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Student Added")
        view_students()
        load_students()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def delete_student():
    selected = student_tree.focus()
    if not selected:
        messagebox.showwarning("Warning", "Select a student to delete")
        return

    data = student_tree.item(selected)["values"]
    student_id = data[0]

    try:
        conn = get_connection()
        cur = conn.cursor()

        # Delete attendance linked to this student
        cur.execute("""
            DELETE FROM Attendance 
            WHERE enrollment_id IN 
            (SELECT enrollment_id FROM Enrollment WHERE student_id=%s)
        """, (student_id,))

        # Delete enrollment
        cur.execute("DELETE FROM Enrollment WHERE student_id=%s", (student_id,))

        # Delete student
        cur.execute("DELETE FROM Student WHERE student_id=%s", (student_id,))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Student Deleted Successfully")
        view_students()
        load_students()
        view_report()

    except Exception as e:
        messagebox.showerror("Error", str(e))

def view_students():
    for row in student_tree.get_children():
        student_tree.delete(row)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Student")
    for row in cur.fetchall():
        student_tree.insert("", "end", values=row)
    conn.close()

tk.Button(student_tab, text="Add Student", bg="#16a34a",
          fg="white", command=add_student).pack(pady=5)

tk.Button(student_tab, text="Delete Student", bg="#dc2626",
          fg="white", command=delete_student).pack(pady=5)

student_tree = create_tree(student_tab,
                           ("Student ID","Roll No","Name","Email","Department"))
view_students()


# ======================================================
# ================= FACULTY TAB ========================
# ======================================================
faculty_tab = tk.Frame(notebook, bg="white")
notebook.add(faculty_tab, text="Faculty")

tk.Label(faculty_tab, text="Name").pack()
fac_name = tk.Entry(faculty_tab)
fac_name.pack()

tk.Label(faculty_tab, text="Email").pack()
fac_email = tk.Entry(faculty_tab)
fac_email.pack()

tk.Label(faculty_tab, text="Department").pack()
fac_dept = tk.Entry(faculty_tab)
fac_dept.pack()

def add_faculty():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO Faculty(name,email,department) VALUES(%s,%s,%s)",
                    (fac_name.get(), fac_email.get(), fac_dept.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Faculty Added")
        view_faculty()
        load_faculty()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def delete_faculty():
    selected = faculty_tree.focus()
    if not selected:
        messagebox.showwarning("Warning", "Select faculty to delete")
        return

    data = faculty_tree.item(selected)["values"]
    faculty_id = data[0]

    try:
        conn = get_connection()
        cur = conn.cursor()

        # Set faculty_id to NULL in Subject first (if allowed)
        cur.execute("UPDATE Subject SET faculty_id=NULL WHERE faculty_id=%s", (faculty_id,))

        cur.execute("DELETE FROM Faculty WHERE faculty_id=%s", (faculty_id,))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Faculty Deleted Successfully")
        view_faculty()
        load_faculty()
        view_report()

    except Exception as e:
        messagebox.showerror("Error", str(e))

def view_faculty():
    for row in faculty_tree.get_children():
        faculty_tree.delete(row)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Faculty")
    for row in cur.fetchall():
        faculty_tree.insert("", "end", values=row)
    conn.close()

tk.Button(faculty_tab, text="Add Faculty",
          bg="#2563eb", fg="white", command=add_faculty).pack(pady=5)

tk.Button(faculty_tab, text="Delete Faculty",
          bg="#dc2626", fg="white", command=delete_faculty).pack(pady=5)

faculty_tree = create_tree(faculty_tab,
                           ("Faculty ID","Name","Email","Department"))
view_faculty()

# ======================================================
# ================= SUBJECT TAB ========================
# ======================================================
subject_tab = tk.Frame(notebook, bg="white")
notebook.add(subject_tab, text="Subject")

tk.Label(subject_tab, text="Subject Name").pack()
sub_name = tk.Entry(subject_tab)
sub_name.pack()

tk.Label(subject_tab, text="Select Faculty").pack()
faculty_combo = ttk.Combobox(subject_tab, state="readonly")
faculty_combo.pack()

def load_faculty():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT faculty_id, name FROM Faculty")
    data = cur.fetchall()
    faculty_combo['values'] = [f"{row[0]} - {row[1]}" for row in data]
    conn.close()

def add_subject():
    try:
        faculty_id = faculty_combo.get().split(" - ")[0]
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO Subject(subject_name,faculty_id) VALUES(%s,%s)",
                    (sub_name.get(), faculty_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Subject Added")
        view_subject()
        load_subjects()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def delete_subject():
    selected = subject_tree.focus()
    if not selected:
        messagebox.showwarning("Warning", "Select a subject to delete")
        return

    data = subject_tree.item(selected)["values"]
    subject_id = data[0]

    try:
        conn = get_connection()
        cur = conn.cursor()

        # Delete attendance through enrollment
        cur.execute("""
            DELETE FROM Attendance
            WHERE enrollment_id IN
            (SELECT enrollment_id FROM Enrollment WHERE subject_id=%s)
        """, (subject_id,))

        # Delete enrollment
        cur.execute("DELETE FROM Enrollment WHERE subject_id=%s", (subject_id,))

        # Delete subject
        cur.execute("DELETE FROM Subject WHERE subject_id=%s", (subject_id,))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Subject Deleted Successfully")
        view_subject()
        load_subjects()
        view_report()

    except Exception as e:
        messagebox.showerror("Error", str(e))

def view_subject():
    for row in subject_tree.get_children():
        subject_tree.delete(row)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Subject")
    for row in cur.fetchall():
        subject_tree.insert("", "end", values=row)
    conn.close()

tk.Button(subject_tab, text="Add Subject",
          bg="#7c3aed", fg="white", command=add_subject).pack(pady=5)

tk.Button(subject_tab, text="Delete Subject",
          bg="#dc2626", fg="white", command=delete_subject).pack(pady=5)

subject_tree = create_tree(subject_tab,
                           ("Subject ID","Subject Name","Faculty ID"))
view_subject()

# ======================================================
# ================= ENROLLMENT TAB =====================
# ======================================================
enroll_tab = tk.Frame(notebook, bg="white")
notebook.add(enroll_tab, text="Enrollment")

tk.Label(enroll_tab, text="Select Student").pack()
student_combo = ttk.Combobox(enroll_tab, state="readonly")
student_combo.pack()

tk.Label(enroll_tab, text="Select Subject").pack()
subject_combo = ttk.Combobox(enroll_tab, state="readonly")
subject_combo.pack()

def load_students():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT student_id, name FROM Student")
    data = cur.fetchall()
    student_combo['values'] = [f"{row[0]} - {row[1]}" for row in data]
    conn.close()

def load_subjects():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT subject_id, subject_name FROM Subject")
    data = cur.fetchall()
    subject_combo['values'] = [f"{row[0]} - {row[1]}" for row in data]
    conn.close()

def add_enrollment():
    try:
        student_id = student_combo.get().split(" - ")[0]
        subject_id = subject_combo.get().split(" - ")[0]
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO Enrollment(student_id,subject_id) VALUES(%s,%s)",
                    (student_id, subject_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Enrollment Added")
        view_enrollment()
        load_enrollments()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def delete_enrollment():
    selected = enroll_tree.focus()
    if not selected:
        messagebox.showwarning("Warning", "Select enrollment to delete")
        return

    data = enroll_tree.item(selected)["values"]
    enrollment_id = data[0]

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM Attendance WHERE enrollment_id=%s", (enrollment_id,))
        cur.execute("DELETE FROM Enrollment WHERE enrollment_id=%s", (enrollment_id,))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Enrollment Deleted Successfully")
        view_enrollment()
        load_enrollments()
        view_report()

    except Exception as e:
        messagebox.showerror("Error", str(e))

def view_enrollment():
    for row in enroll_tree.get_children():
        enroll_tree.delete(row)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Enrollment")
    for row in cur.fetchall():
        enroll_tree.insert("", "end", values=row)
    conn.close()

tk.Button(enroll_tab, text="Add Enrollment",
          bg="#10b981", fg="white", command=add_enrollment).pack(pady=5)

tk.Button(enroll_tab, text="Delete Enrollment",
          bg="#dc2626", fg="white", command=delete_enrollment).pack(pady=5)

enroll_tree = create_tree(enroll_tab,
                          ("Enrollment ID","Student ID","Subject ID"))
view_enrollment()

# ======================================================
# ================= ATTENDANCE TAB =====================
# ======================================================
attendance_tab = tk.Frame(notebook, bg="white")
notebook.add(attendance_tab, text="Attendance")

tk.Label(attendance_tab, text="Select Enrollment").pack()
enroll_combo = ttk.Combobox(attendance_tab, state="readonly")
enroll_combo.pack()

tk.Label(attendance_tab, text="Date (YYYY-MM-DD)").pack()
date_entry = tk.Entry(attendance_tab)
date_entry.pack()

tk.Label(attendance_tab, text="Status").pack()
status_combo = ttk.Combobox(attendance_tab,
                            values=["Present","Absent"],
                            state="readonly")
status_combo.pack()

def load_enrollments():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT enrollment_id FROM Enrollment")
    data = cur.fetchall()
    enroll_combo['values'] = [row[0] for row in data]
    conn.close()

def mark_attendance():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.callproc("MarkAttendance",
                     (enroll_combo.get(), date_entry.get(), status_combo.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Attendance Marked")
        view_attendance()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def delete_attendance():
    selected = attendance_tree.focus()
    if not selected:
        messagebox.showwarning("Warning", "Select attendance to delete")
        return

    data = attendance_tree.item(selected)["values"]
    attendance_id = data[0]

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM Attendance WHERE attendance_id=%s", (attendance_id,))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Attendance Deleted Successfully")
        view_attendance()
        view_report()

    except Exception as e:
        messagebox.showerror("Error", str(e))

def view_attendance():
    for row in attendance_tree.get_children():
        attendance_tree.delete(row)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Attendance")
    for row in cur.fetchall():
        attendance_tree.insert("", "end", values=row)
    conn.close()

tk.Button(attendance_tab, text="Mark Attendance",
          bg="#0ea5e9", fg="white", command=mark_attendance).pack(pady=5)

tk.Button(attendance_tab, text="Delete Attendance",
          bg="#dc2626", fg="white", command=delete_attendance).pack(pady=5)

attendance_tree = create_tree(attendance_tab,
                               ("Attendance ID","Enrollment ID","Date","Status"))
view_attendance()


# ---------------- INITIAL LOAD ----------------
load_students()
load_subjects()
load_faculty()
load_enrollments()

# ---------------- ATTENDANCE-VIEW TAB ------------
report_tab = tk.Frame(notebook, bg="white")
notebook.add(report_tab, text="View Attendance")

search_frame = tk.Frame(report_tab, bg="white")
search_frame.pack(pady=10)

tk.Label(search_frame, text="Search by Roll No:",
         bg="white").grid(row=0, column=0, padx=5)

search_entry = tk.Entry(search_frame)
search_entry.grid(row=0, column=1, padx=5)

report_tree = ttk.Treeview(report_tab,
                           columns=("Student ID","Roll No","Student Name",
                                    "Department","Faculty Name",
                                    "Subject","Date","Status"),
                           show="headings")

for col in report_tree["columns"]:
    report_tree.heading(col, text=col)
    report_tree.column(col, width=140)

report_tree.pack(fill="both", expand=True, pady=10)

def view_report():
    for row in report_tree.get_children():
        report_tree.delete(row)

    conn = get_connection()
    cur = conn.cursor()

    query = """
    SELECT 
        s.student_id,
        s.roll_no,
        s.name,
        s.department,
        f.name,
        sub.subject_name,
        a.date,
        a.status
    FROM Student s
    LEFT JOIN Enrollment e ON s.student_id = e.student_id
    LEFT JOIN Subject sub ON e.subject_id = sub.subject_id
    LEFT JOIN Faculty f ON sub.faculty_id = f.faculty_id
    LEFT JOIN Attendance a ON e.enrollment_id = a.enrollment_id
    """

    if search_entry.get() != "":
        query += " WHERE s.roll_no = %s"
        cur.execute(query, (search_entry.get(),))
    else:
        cur.execute(query)

    for row in cur.fetchall():
        report_tree.insert("", "end", values=row)

    conn.close()

tk.Button(search_frame, text="Search",
          bg="#2563eb", fg="white",
          command=view_report).grid(row=0, column=2, padx=5)

tk.Button(search_frame, text="Show All",
          bg="#10b981", fg="white",
          command=view_report).grid(row=0, column=3, padx=5)

view_report()

root.mainloop()
