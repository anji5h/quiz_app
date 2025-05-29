import tkinter as tk
from frames.quiz_frame import QuizFrame
from frames.leaderboard_frame import LeaderboardFrame


class UserFrame(tk.Frame):
    """Frame for user functionalities."""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.configure(bg="#f0f0f0")
        self.setup_ui()

    def setup_ui(self):
        self.pack(fill="both", expand=True)
        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.pack(expand=True)

        # Title
        tk.Label(
            main_frame,
            text=f"Welcome, {self.app.current_user.username}",
            font=("Arial", 24, "bold"),
            bg="#f0f0f0",
            fg="#333333",
        ).pack(pady=(20, 40))

        tk.Button(
            main_frame,
            text="Take Quiz",
            command=self.show_quiz,
            font=("Arial", 12),
            bg="#4CAF50",  # Green
            fg="white",
            width=20,
            padx=10,
            pady=5,
        ).pack(pady=10)

        tk.Button(
            main_frame,
            text="View Leaderboard",
            command=self.show_leaderboard,
            font=("Arial", 12),
            bg="#2196F3",  # Blue
            fg="white",
            width=20,
            padx=10,
            pady=5,
        ).pack(pady=10)

        tk.Button(
            main_frame,
            text="Logout",
            command=self.app.show_auth_frame,
            font=("Arial", 12),
            bg="#F44336",
            fg="white",
            width=20,
            padx=10,
            pady=5,
        ).pack(pady=10)

    def show_quiz(self):
        self.app.clear_frame()
        self.app.current_frame = QuizFrame(self.app.root, self.app, self)
        self.app.current_frame.pack(fill="both", expand=True)

    def show_leaderboard(self):
        self.app.clear_frame()
        self.app.current_frame = LeaderboardFrame(self.app.root, self.app, self)
        self.app.current_frame.pack(fill="both", expand=True)
