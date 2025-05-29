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
        self.configure(bg="#f0f0f0")
        self.setup_ui()

    def setup_ui(self):
        config = self.app.data_manager.load_config()
        if not config:
            self.app.show_auth_frame()
            return

        self.pack(fill="both", expand=True)

        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.pack(expand=True)

        # Title
        tk.Label(
            main_frame,
            text="Select a Topic",
            font=("Arial", 24, "bold"),
            bg="#f0f0f0",
            fg="#333333",
        ).pack(pady=(20, 20))

        # Topic Selection
        self.topic_var = tk.StringVar()
        topics = config.topics
        if not topics:
            messagebox.showerror("Error", "No topics available")
            self.back()
            return
        topic_combo = ttk.Combobox(
            main_frame,
            textvariable=self.topic_var,
            values=[t.replace("_", " ").title() for t in topics],
            state="readonly",
            width=30,
            font=("Arial", 12),
        )
        topic_combo.pack(pady=5)

        tk.Button(
            main_frame,
            text="Start Quiz",
            command=self.start_quiz,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            width=20,
            padx=10,
            pady=5,
        ).pack(pady=10)

        tk.Button(
            main_frame,
            text="Back",
            command=self.back,
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            width=20,
            padx=10,
            pady=5,
        ).pack(pady=5)

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

        self.pack(fill="both", expand=True)

        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.pack(expand=True)

        if self.current_question >= len(self.questions):
            self.show_results()
            return

        question = self.questions[self.current_question]
        tk.Label(
            main_frame,
            text=f"Question {self.current_question + 1}: {question.question}",
            font=("Arial", 14, "bold"),
            bg="#f0f0f0",
            fg="#333333",
            wraplength=700,
        ).pack(pady=(20, 10))

        self.selected_answer.set(" ")
        for key in sorted(question.options.keys()):
            tk.Radiobutton(
                main_frame,
                text=question.options[key],
                variable=self.selected_answer,
                value=key,
                font=("Arial", 12),
                bg="#f0f0f0",
                fg="#333333",
                anchor="w",
                padx=30,
            ).pack(fill="x", pady=5)

        tk.Button(
            main_frame,
            text="Submit",
            command=self.submit_answer,
            font=("Arial", 12),
            bg="#FF9800",
            fg="white",
            width=20,
            padx=10,
            pady=5,
        ).pack(pady=20)

    def submit_answer(self):
        if not self.selected_answer.get():
            messagebox.showerror("Error", "Please select an answer")
            return
        question = self.questions[self.current_question]
        if self.selected_answer.get() == question.answer:
            self.score += 1
        self.current_question += 1
        self.show_question()

    def show_results(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.pack(fill="both", expand=True)

        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.pack(expand=True)

        topic = self.topic_var.get().lower().replace(" ", "_")
        tk.Label(
            main_frame,
            text=f"Your Score: {self.score}/{len(self.questions)}",
            font=("Arial", 24, "bold"),
            bg="#f0f0f0",
            fg="#333333",
        ).pack(pady=(20, 10))

        if self.app.data_manager.save_score(
            self.app.current_user.username, topic, self.score, len(self.questions)
        ):
            tk.Label(
                main_frame,
                text="Score saved successfully!",
                font=("Arial", 12),
                bg="#f0f0f0",
                fg="#333333",
            ).pack(pady=10)

        tk.Button(
            main_frame,
            text="Back",
            command=self.back,
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            width=20,
            padx=10,
            pady=5,
        ).pack(pady=20)

    def back(self):
        self.app.show_user_frame()
