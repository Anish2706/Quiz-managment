import tkinter as tk
from tkinter import messagebox
import mysql.connector
import random

class QuizManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Management System")

        self.username_label = tk.Label(root, text="Username:")
        self.username_entry = tk.Entry(root)

        self.password_label = tk.Label(root, text="Password:")
        self.password_entry = tk.Entry(root, show="*")

        self.login_button = tk.Button(root, text="Login", command=self.login)

        self.username_label.pack()
        self.username_entry.pack()
        self.password_label.pack()
        self.password_entry.pack()
        self.login_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Simulate teacher and student login
        if username == "teacher" and password == "password":
            self.show_teacher_interface()
        elif username == "student" and password == "password":
            self.show_student_interface()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def show_teacher_interface(self):
        self.clear_login_screen()
        teacher_label = tk.Label(self.root, text="Welcome, Teacher!")
        add_question_button = tk.Button(self.root, text="Add Question", command=self.add_question)

        teacher_label.pack()
        add_question_button.pack()

    def show_student_interface(self):
        self.clear_login_screen()
        student_label = tk.Label(self.root, text="Welcome, Student!")
        attempt_quiz_button = tk.Button(self.root, text="Attempt Quiz", command=self.attempt_quiz)

        student_label.pack()
        attempt_quiz_button.pack()

    def clear_login_screen(self):
        self.username_label.pack_forget()
        self.username_entry.pack_forget()
        self.password_label.pack_forget()
        self.password_entry.pack_forget()
        self.login_button.pack_forget()

    def add_question(self):
        # Create a new window for adding a question
        add_question_window = tk.Toplevel(self.root)
        add_question_window.title("Add Question")

        question_label = tk.Label(add_question_window, text="Enter the question:")
        question_entry = tk.Entry(add_question_window)

        op1_label = tk.Label(add_question_window, text="Enter option A:")
        op1_entry = tk.Entry(add_question_window)

        op2_label = tk.Label(add_question_window, text="Enter option B:")
        op2_entry = tk.Entry(add_question_window)

        op3_label = tk.Label(add_question_window, text="Enter option C:")
        op3_entry = tk.Entry(add_question_window)

        ans_label = tk.Label(add_question_window, text="Enter the correct option:")
        ans_entry = tk.Entry(add_question_window)

        add_button = tk.Button(add_question_window, text="Add Question", command=lambda: self.add_question_to_db(
            question_entry.get(), op1_entry.get(), op2_entry.get(), op3_entry.get(), ans_entry.get()))

        question_label.pack()
        question_entry.pack()
        op1_label.pack()
        op1_entry.pack()
        op2_label.pack()
        op2_entry.pack()
        op3_label.pack()
        op3_entry.pack()
        ans_label.pack()
        ans_entry.pack()
        add_button.pack()

    def add_question_to_db(self, question, op1, op2, op3, ans):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="quiz", charset='utf8'
            )

            cursor = connection.cursor()

            # Get the current maximum question_number
            cursor.execute("SELECT MAX(qno) FROM question")
            max_question_number = cursor.fetchone()[0]
            qno = max_question_number + 1 if max_question_number is not None else 1

            # Insert the question into the database
            cursor.execute("INSERT INTO question VALUES (%s, %s, %s, %s, %s, %s)", (qno, question, op1, op2, op3, ans))
            connection.commit()

            messagebox.showinfo("Success", "Question added successfully")

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")

        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    def attempt_quiz(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
            database="quiz", charset='utf8'
        )

            mycursor = connection.cursor()

            print("Welcome to Quiz portal")
            print("***********************")
            mycursor.execute("SELECT * FROM question")
            data = mycursor.fetchall()

            name = input("Enter your name: ")
            rc = mycursor.rowcount
            noq = int(input("Enter the number of questions to attempt (max %s):" % rc))
            l = []
            user_responses = []

            while len(l) != noq:
                x = random.randint(1, rc)
                if x not in l:
                    l.append(x)

            print("Quiz has started")
            c = 1
            score = 0

            for i in range(0, len(l)):
                mycursor.execute("Select * from question where qno=%s", (l[i],))
                ques = mycursor.fetchone()
    
                print("--------------------------------------------------------------------------------------------")
                print(f"Q.{c}: {ques[1]}\nA.{ques[2]}\t\tB.{ques[3]}\nC.{ques[4]}")
                print("--------------------------------------------------------------------------------------------")
                c += 1
                ans = None

                while ans is None:
                    choice = input("Answer (A, B, C): ")
                    if choice.upper() in {'A', 'B', 'C'}:
                        ans = choice
                    else:
                        print("Kindly select A, B, C as option only")

                user_responses.append((ques[1], ans, ques[5]))  # Store user's response and correct answer

                if ans == ques[5]:
                    
                    score += 1

            print("Quiz has ended!! Your final score is:", score)
            print("Answers:")
            for response in user_responses:
                print(f"Q: {response[0]}\nYour Answer: {response[1]}\tCorrect Answer: {response[2]}\n")
    
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")

        finally:
            if connection and connection.is_connected():
                mycursor.close()
                connection.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizManagementSystem(root)
    root.mainloop()
