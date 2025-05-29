import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from schemas import Result


class LeaderboardFrame(tk.Frame):
    """Frame for displaying leaderboard."""

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
            text="Leaderboard",
            font=("Arial", 24, "bold"),
            bg="#f0f0f0",
            fg="#333333",
        ).pack(pady=(20, 20))

        # Topic Selection
        tk.Label(
            main_frame,
            text="Select Topic",
            font=("Arial", 12),
            bg="#f0f0f0",
            fg="#333333",
        ).pack(pady=(0, 5))
        self.topic_var = tk.StringVar(value="All")
        topic_combo = ttk.Combobox(
            main_frame,
            textvariable=self.topic_var,
            values=["All"]
            + [
                t.replace("_", " ").title()
                for t in self.app.data_manager.load_config().topics
            ],
            state="readonly",
            width=30,
            font=("Arial", 12),
        )
        topic_combo.pack(pady=5)

        self.topic_var.trace_add("write", self.on_topic_change)

        # Treeview for leaderboard
        self.tree = ttk.Treeview(
            main_frame,
            columns=("Username", "Score", "Percentage"),
            show="headings",
            style="Treeview",
        )
        self.tree.heading("Username", text="Username")
        self.tree.heading("Score", text="Score")
        self.tree.heading("Percentage", text="Percentage (%)")

        self.tree.column("Username", anchor="center", width=150)
        self.tree.column("Score", anchor="center", width=150)
        self.tree.column("Percentage", anchor="center", width=150)
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Button(
            main_frame,
            text="Back",
            command=self.back,
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            width=10,
            padx=10,
            pady=5,
        ).pack(pady=10)

        self.show_leaderboard()

    def on_topic_change(self, *args):
        """Update the leaderboard when the topic selection changes."""
        self.show_leaderboard()

    def show_leaderboard(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        topic = self.topic_var.get().lower().replace(" ", "_")
        if topic == "all":
            result_data = self.app.data_manager.load_json_file(
                self.app.data_manager.scores_path
            )
            if not result_data:
                return
            try:
                result = Result.model_validate(result_data)
                aggregated = {}
                for username, user_data in result.root.items():
                    best_score = 0
                    total_questions = 0
                    for topic_scores in user_data.root.values():
                        best = max(
                            topic_scores,
                            key=lambda x: x.score / x.total if x.total > 0 else 0,
                            default=None,
                        )
                        if best:
                            best_score += best.score
                            total_questions += best.total
                    if total_questions > 0:
                        aggregated[username] = {
                            "username": username,
                            "score": f"{best_score}/{total_questions}",
                            "percentage": (
                                (best_score / total_questions * 100)
                                if total_questions > 0
                                else 0
                            ),
                        }
                leaderboard = sorted(
                    aggregated.values(), key=lambda x: x["percentage"], reverse=True
                )
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Error processing all topics leaderboard: {str(e)}"
                )
                return
        else:
            leaderboard = self.app.data_manager.get_leaderboard(topic)
        for entry in leaderboard:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    entry["username"],
                    entry["score"],
                    f"{entry['percentage']:.2f}",
                ),
            )

    def back(self):
        if self.parent_frame.__class__.__name__ == "UserFrame":
            self.app.show_user_frame()
        elif self.parent_frame.__class__.__name__ == "AdminFrame":
            self.app.show_admin_frame()
