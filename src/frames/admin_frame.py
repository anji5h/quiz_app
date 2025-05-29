import tkinter as tk
from frames.manage_questions_frame import ManageQuestionsFrame
from frames.leaderboard_frame import LeaderboardFrame
from frames.analytics_frame import AnalyticsFrame


class AdminFrame(tk.Frame):
    """Frame for admin functionalities."""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.setup_ui()

    def setup_ui(self):
        tk.Label(
            self,
            text=f"Admin Dashboard",
            font=("Arial", 16),
        ).pack(pady=10)
        tk.Button(
            self, text="Manage Questions", command=self.show_manage_questions
        ).pack(pady=5)
        tk.Button(self, text="View Leaderboard", command=self.show_leaderboard).pack(
            pady=5
        )
        tk.Button(self, text="View Analytics", command=self.show_analytics).pack(pady=5)
        tk.Button(self, text="Logout", command=self.app.show_auth_frame).pack(pady=5)

    def show_manage_questions(self):
        self.app.clear_frame()
        self.app.current_frame = ManageQuestionsFrame(self.app.root, self.app, self)
        self.app.current_frame.pack(fill="both", expand=True)

    def show_leaderboard(self):
        self.app.clear_frame()
        self.app.current_frame = LeaderboardFrame(self.app.root, self.app, self)
        self.app.current_frame.pack(fill="both", expand=True)

    def show_analytics(self):
        self.app.clear_frame()
        self.app.current_frame = AnalyticsFrame(self.app.root, self.app, self)
        self.app.current_frame.pack(fill="both", expand=True)
