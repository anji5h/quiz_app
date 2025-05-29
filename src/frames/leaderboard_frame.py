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
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self, text="Leaderboard", font=("Arial", 16)).pack(pady=10)
        config = self.app.data_manager.load_config()
        if not config:
            self.back()
            return
        tk.Label(self, text="Select Topic").pack()
        self.topic_var = tk.StringVar()
        topics = config.topics
        ttk.Combobox(
            self,
            textvariable=self.topic_var,
            values=["All"] + [t.replace("_", " ").title() for t in topics],
            state="readonly",
        ).pack(pady=5)
        tk.Button(self, text="Show Leaderboard", command=self.show_leaderboard).pack(
            pady=5
        )
        tk.Button(self, text="Back", command=self.back).pack(pady=5)
        self.tree = ttk.Treeview(
            self, columns=("Username", "Score", "Total", "Percentage"), show="headings"
        )
        self.tree.heading("Username", text="Username")
        self.tree.heading("Score", text="Score")
        self.tree.heading("Total", text="Total")
        self.tree.heading("Percentage", text="Percentage (%)")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

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
                            "score": best_score,
                            "total": total_questions,
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
                    entry["total"],
                    f"{entry['percentage']:.2f}",
                ),
            )

    def back(self):
        self.app.clear_frame()
        self.app.current_frame = self.parent_frame
        self.app.current_frame.pack(fill="both", expand=True)