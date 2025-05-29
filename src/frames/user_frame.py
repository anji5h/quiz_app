import tkinter as tk
from frames.quiz_frame import QuizFrame
from frames.leaderboard_frame import LeaderboardFrame


class UserFrame(tk.Frame):
    """Frame for user functionalities."""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.setup_ui()

    def setup_ui(self):
        tk.Label(
            self, text=f"Welcome, {self.app.current_user.username}", font=("Arial", 16)
        ).pack(pady=10)
        tk.Button(self, text="Take Quiz", command=self.show_quiz).pack(pady=5)
        tk.Button(self, text="View Leaderboard", command=self.show_leaderboard).pack(
            pady=5
        )
        tk.Button(self, text="Logout", command=self.app.show_auth_frame).pack(pady=5)

    def show_quiz(self):
        self.app.clear_frame()
        self.app.current_frame = QuizFrame(self.app.root, self.app, self)
        self.app.current_frame.pack(fill="both", expand=True)

    def show_leaderboard(self):
        self.app.clear_frame()
        self.app.current_frame = LeaderboardFrame(self.app.root, self.app, self)
        self.app.current_frame.pack(fill="both", expand=True)
