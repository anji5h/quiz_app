import tkinter as tk
from tkinter import ttk
from frames.add_question_frame import AddQuestionFrame
from frames.delete_question_frame import DeleteQuestionFrame

class ManageQuestionsFrame(tk.Frame):
    """Frame for adding/deleting questions."""

    def __init__(self, parent, app, parent_frame):
        super().__init__(parent)
        self.app = app
        self.parent_frame = parent_frame
        self.configure(bg="#f0f0f0")
        self.setup_ui()

    def setup_ui(self):
        self.pack(fill="both", expand=True)

        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.pack(expand=True)

        # Title
        tk.Label(
            main_frame,
            text="Manage Questions",
            font=("Arial", 24, "bold"),
            bg="#f0f0f0",
            fg="#333333",
        ).pack(pady=(20, 40))

        tk.Button(
            main_frame,
            text="Add Question",
            command=self.show_add_question,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            width=20,
            padx=10,
            pady=5,
        ).pack(pady=10)

        tk.Button(
            main_frame,
            text="Delete Question",
            command=self.show_delete_question,
            font=("Arial", 12),
            bg="#F44336",
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
        ).pack(pady=10)

    def show_add_question(self):
        self.app.clear_frame()
        self.app.current_frame = AddQuestionFrame(self.app.root, self.app, self)
        self.app.current_frame.pack(fill="both", expand=True)

    def show_delete_question(self):
        self.app.clear_frame()
        self.app.current_frame = DeleteQuestionFrame(self.app.root, self.app, self)
        self.app.current_frame.pack(fill="both", expand=True)

    def back(self):
        self.app.show_admin_frame()