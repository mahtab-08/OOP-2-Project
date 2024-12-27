import csv
import os

class Student:
    def __init__(self, student_id, name, email):
        self.student_id = student_id
        self.name = name
        self.email = email

    def to_dict(self):
        return {"Student ID": self.student_id, "Name": self.name, "Email": self.email}

class Course:
    def __init__(self, course_id, course_name, credits):
        self.course_id = course_id
        self.course_name = course_name
        self.credits = credits

    def to_dict(self):
        return {"Course ID": self.course_id, "Course Name": self.course_name, "Credits": self.credits}

class Grade:
    def __init__(self, student_id, course_id, grade):
        self.student_id = student_id
        self.course_id = course_id
        self.grade = grade

    def to_dict(self):
        return {"Student ID": self.student_id, "Course ID": self.course_id, "Grade": self.grade}

def load_data(file_name):
    if not os.path.exists(file_name):
        with open(file_name, 'w') as f:
            f.write("Students.csv,Courses.csv,Grades.csv")
        open("Students.csv", 'w').close()
        open("Courses.csv", 'w').close()
        open("Grades.csv", 'w').close()

    students = []
    courses = []
    grades = []

    # Load Students
    if os.path.exists("Students.csv"):
        with open("Students.csv", 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                students.append(Student(row['Student ID'], row['Name'], row['Email']))

    # Load Courses
    if os.path.exists("Courses.csv"):
        with open("Courses.csv", 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                courses.append(Course(row['Course ID'], row['Course Name'], row['Credits']))

    # Load Grades
    if os.path.exists("Grades.csv"):
        with open("Grades.csv", 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                grades.append(Grade(row['Student ID'], row['Course ID'], row['Grade']))

    return students, courses, grades

def save_data():
    # Save Students
    with open("Students.csv", 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Student ID", "Name", "Email"])
        writer.writeheader()
        for student in students:
            writer.writerow(student.to_dict())

    # Save Courses
    with open("Courses.csv", 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Course ID", "Course Name", "Credits"])
        writer.writeheader()
        for course in courses:
            writer.writerow(course.to_dict())

    # Save Grades
    with open("Grades.csv", 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Student ID", "Course ID", "Grade"])
        writer.writeheader()
        for grade in grades:
            writer.writerow(grade.to_dict())

# Main Program
students, courses, grades = load_data("data_config.csv")

while True:
    print("\nWelcome to the Student Management System!")
    print("1. Add a new student")
    print("2. Add a new course")
    print("3. Assign a grade")
    print("4. View student records")
    print("5. Exit")
    option = input("Choose an option: ")

    if option == "1":  
        student_id = input("Enter Student ID: ")
        if any(student.student_id == student_id for student in students):
            print("Error: A student with this ID already exists.")
        else:
            name = input("Enter Student Name: ")
            email = input("Enter Student Email: ")
            students.append(Student(student_id, name, email))
            save_data()
            print("Student added successfully!")

    elif option == "2":  
        course_id = input("Enter Course ID: ")
        if any(course.course_id == course_id for course in courses):
            print("Error: A course with this ID already exists.")
        else:
            course_name = input("Enter Course Name: ")
            credits = input("Enter Credits: ")
            courses.append(Course(course_id, course_name, credits))
            save_data()
            print("Course added successfully!")

    elif option == "3":  
        student_id = input("Enter Student ID: ")
        course_id = input("Enter Course ID: ")
        grade = input("Enter Grade: ")

        if any(g.student_id == student_id and g.course_id == course_id for g in grades):
            print("Error: Grade for this student in this course already exists.")
        else:
            if (any(s.student_id == student_id for s in students) and 
                any(c.course_id == course_id for c in courses)):
                grades.append(Grade(student_id, course_id, grade))
                save_data()
                print("Grade assigned successfully!")
            else:
                print("Error: Invalid Student ID or Course ID.")

    elif option == "4":  
        print("\nStudent Records:")
        for student in students:
            print(f"ID: {student.student_id}, Name: {student.name}, Email: {student.email}")
            student_grades = [
                (g.course_id, g.grade) for g in grades if g.student_id == student.student_id
            ]
            if student_grades:
                print("  Grades:")
                for course_id, grade in student_grades:
                    course_name = next((c.course_name for c in courses if c.course_id == course_id), "Unknown Course")
                    print(f"    - Course: {course_name}, Grade: {grade}")
            else:
                print("  Grades: None")

    elif option == "5":
        save_data()  
        print("Exiting... Goodbye!")
        break

    else:
        print("Invalid option. Please try again.")
