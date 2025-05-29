import tkinter as tk
from tkinter import ttk


class AnalyticsFrame(tk.Frame):
    """Frame for displaying analytics."""

    def __init__(self, parent, app, parent_frame):
        super().__init__(parent)
        self.app = app
        self.parent_frame = parent_frame
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
            text="Analytics",
            font=("Arial", 24, "bold"),
            bg="#f0f0f0",
            fg="#333333",
        ).pack(pady=(20, 20))

        # Grid for main metrics
        metrics_frame = tk.Frame(main_frame, bg="#f0f0f0")
        metrics_frame.pack(pady=10)

        analytics = self.app.data_manager.get_analytics()
        tk.Label(
            metrics_frame,
            text=f"Total Users: {analytics['total_users']}",
            font=("Arial", 12),
            bg="#f0f0f0",
            fg="#333333",
            width=15,
            anchor="center",
        ).grid(row=0, column=0, padx=10, pady=5)
        tk.Label(
            metrics_frame,
            text=f"Total Topics: {analytics['total_topics']}",
            font=("Arial", 12),
            bg="#f0f0f0",
            fg="#333333",
            width=15,
            anchor="center",
        ).grid(row=0, column=1, padx=10, pady=5)
        tk.Label(
            metrics_frame,
            text=f"Active User: {analytics['users_took_quizzes']}",
            font=("Arial", 12),
            bg="#f0f0f0",
            fg="#333333",
            width=15,
            anchor="center",
        ).grid(row=0, column=2, padx=10, pady=5)

        # Per-Topic Activity Table
        tk.Label(
            main_frame,
            text="Per-Topic Activity:",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            fg="#333333",
        ).pack(pady=(10, 5))
        tree_frame = tk.Frame(main_frame, bg="#f0f0f0")
        tree_frame.pack(pady=10, fill="x")
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("Topic", "Users"),
            show="headings",
            height=10,
        )
        self.tree.heading("Topic", text="Topic")
        self.tree.heading("Users", text="Users")
        self.tree.column("Topic", anchor="center", width=200)
        self.tree.column("Users", anchor="center", width=100)
        self.tree.pack(fill="x", padx=20)

        for topic, count in analytics["per_topic_activity"].items():
            self.tree.insert(
                "", tk.END, values=(topic.replace("_", " ").title(), count)
            )

        # Back button
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
        self.app.clear_frame()
        self.app.current_frame = self.parent_frame
        self.app.current_frame.pack(fill="both", expand=True)
