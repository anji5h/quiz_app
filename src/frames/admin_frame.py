import tkinter as tk
from frames.manage_questions_frame import ManageQuestionsFrame
from frames.leaderboard_frame import LeaderboardFrame
from frames.analytics_frame import AnalyticsFrame


class AdminFrame(tk.Frame):
    """Frame for admin functionalities."""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.configure(bg="#f0f0f0")  # Light gray background for consistency
        self.setup_ui()

    def setup_ui(self):
        # Center the frame content
        self.pack(fill="both", expand=True)

        # Main container frame with padding
        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.pack(expand=True)

        # Title
        tk.Label(
            main_frame,
            text="Admin Dashboard",
            font=("Arial", 24, "bold"),
            bg="#f0f0f0",
            fg="#333333",
        ).pack(pady=(20, 40))

        # Buttons with distinct colors and centered layout
        tk.Button(
            main_frame,
            text="Manage Questions",
            command=self.show_manage_questions,
            font=("Arial", 12),
            bg="#FF9800",  # Orange
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
            text="View Analytics",
            command=self.show_analytics,
            font=("Arial", 12),
            bg="#4CAF50",  # Green
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
            bg="#F44336",  # Red
            fg="white",
            width=20,
            padx=10,
            pady=5,
        ).pack(pady=10)

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
