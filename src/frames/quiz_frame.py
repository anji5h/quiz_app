import tkinter as tk
from tkinter import messagebox, ttk

class QuizFrame(tk.Frame):
    """Frame for taking a quiz."""

    def __init__(self, parent, app, parent_frame):
        super().__init__(parent)
        self.app = app
        self.parent_frame = parent_frame
        self.questions = []
        self.current_question = 0
        self.score = 0
        self.selected_answer = tk.StringVar()
        self.setup_ui()

    def setup_ui(self):
        config = self.app.data_manager.load_config()
        if not config:
            self.app.show_auth_frame()
            return
        tk.Label(self, text="Select a Topic", font=("Arial", 14)).pack(pady=10)
        self.topic_var = tk.StringVar()
        topics = config.topics
        if not topics:
            messagebox.showerror("Error", "No topics available")
            self.back()
            return
        ttk.Combobox(
            self,
            textvariable=self.topic_var,
            values=[t.replace("_", " ").title() for t in topics],
            state="readonly",
        ).pack(pady=5)
        tk.Button(self, text="Start Quiz", command=self.start_quiz).pack(pady=10)
        tk.Button(self, text="Back", command=self.back).pack(pady=5)

    def start_quiz(self):
        topic = self.topic_var.get().lower().replace(" ", "_")
        if not topic:
            messagebox.showerror("Error", "Please select a topic")
            return
        self.questions = self.app.data_manager.load_questions(topic)
        if not self.questions:
            self.back()
            return
        self.score = 0
        self.current_question = 0
        self.show_question()

    def show_question(self):
        for widget in self.winfo_children():
            widget.destroy()
        if self.current_question >= len(self.questions):
            self.show_results()
            return
        question = self.questions[self.current_question]
        tk.Label(
            self,
            text=f"Question {self.current_question + 1}: {question.question}",
            font=("Arial", 12),
            wraplength=700,
        ).pack(pady=10)
        self.selected_answer.set(" ")
        for key in sorted(question.options.keys()):
            tk.Radiobutton(
                self,
                text=question.options[key],
                variable=self.selected_answer,
                value=key,
            ).pack(anchor="w", padx=20)
        tk.Button(self, text="Submit", command=self.submit_answer).pack(pady=10)

    def submit_answer(self):
        if not self.selected_answer.get():
            messagebox.showerror("Error", "Please select an answer")
            return
        question = self.questions[self.current_question]
        if self.selected_answer.get() == question.answer:
            self.score += 1
            messagebox.showinfo("Feedback", "Correct Answer!")
        else:
            messagebox.showinfo(
                "Feedback",
                f"Oops!! Wrong Answer",
            )
        self.current_question += 1
        self.show_question()

    def show_results(self):
        for widget in self.winfo_children():
            widget.destroy()
        topic = self.topic_var.get().lower().replace(" ", "_")
        tk.Label(
            self,
            text=f"Your Score: {self.score}/{len(self.questions)}",
            font=("Arial", 14),
        ).pack(pady=20)
        if self.app.data_manager.save_score(
            self.app.current_user.username, topic, self.score, len(self.questions)
        ):
            tk.Label(self, text="Score saved successfully!", font=("Arial", 12)).pack(
                pady=10
            )
        tk.Button(self, text="Back", command=self.back).pack(pady=5)

    def back(self):
        self.app.show_user_frame()
