import tkinter as tk


class AnalyticsFrame(tk.Frame):
    """Frame for displaying analytics."""

    def __init__(self, parent, app, parent_frame):
        super().__init__(parent)
        self.app = app
        self.parent_frame = parent_frame
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self, text="Analytics", font=("Arial", 16)).pack(pady=10)
        analytics = self.app.data_manager.get_analytics()
        tk.Label(self, text=f"Total Users: {analytics['total_users']}").pack(pady=5)
        tk.Label(self, text=f"Total Topics: {analytics['total_topics']}").pack(pady=5)
        tk.Label(
            self, text=f"Users Who Took Quizzes: {analytics['users_took_quizzes']}"
        ).pack(pady=5)
        tk.Label(self, text="Per-Topic Activity:").pack(pady=5)
        for topic, count in analytics["per_topic_activity"].items():
            tk.Label(
                self, text=f"{topic.replace('_', ' ').title()}: {count} users"
            ).pack(anchor="w", padx=20)
        tk.Button(self, text="Back", command=self.back).pack(pady=10)

    def back(self):
        self.app.clear_frame()
        self.app.current_frame = self.parent_frame
        self.app.current_frame.pack(fill="both", expand=True)
