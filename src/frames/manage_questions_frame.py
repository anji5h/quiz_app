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
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self, text="Manage Questions", font=("Arial", 16)).pack(pady=10)
        config = self.app.data_manager.load_config()
        if not config:
            self.back()
            return
        tk.Button(self, text="Add Question", command=self.show_add_question).pack(
            pady=5
        )
        tk.Button(self, text="Delete Question", command=self.show_delete_question).pack(
            pady=5
        )
        tk.Button(self, text="Back", command=self.back).pack(pady=5)

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
