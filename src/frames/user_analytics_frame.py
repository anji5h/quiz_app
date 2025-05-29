import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from schemas import Score


class UserAnalyticsFrame(tk.Frame):
    """Frame for displaying user score progression over time for all topics using Matplotlib and Seaborn."""

    def __init__(self, parent, app, parent_frame):
        super().__init__(parent)
        self.app = app
        self.parent_frame = parent_frame
        self.configure(bg="#f0f0f0")
        self.canvas = None
        self.setup_ui()

    def setup_ui(self):
        self.pack(fill="both", expand=True)

        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.pack(expand=True, fill="both")

        # Title
        tk.Label(
            main_frame,
            text="User Analytics",
            font=("Arial", 24, "bold"),
            bg="#f0f0f0",
            fg="#333333",
        ).pack(pady=(20, 20))

        self.chart_frame = tk.Frame(main_frame, bg="#f0f0f0")
        self.chart_frame.pack(pady=10, fill="both", expand=True)

        # Back Button
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

        self.load_data()

    def load_data(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        username = self.app.current_user.username
        all_scores = self.app.data_manager.get_user_scores(username)
        if not all_scores:
            messagebox.showinfo("Info", "No score data available")
            self.back()
            return

        for topic, scores in all_scores.items():
            for score in scores:
                if isinstance(score, dict):
                    score["timestamp"] = datetime.fromisoformat(score["timestamp"])
                elif isinstance(score, Score):
                    score.timestamp = datetime.fromisoformat(score.timestamp)

        self.draw_chart(all_scores)

    def draw_chart(self, all_scores):
        sns.set_theme(style="whitegrid", palette="deep")

        fig, ax = plt.subplots(figsize=(8, 4))

        all_timestamps = set()
        for scores in all_scores.values():
            all_timestamps.update(
                s["timestamp"] if isinstance(s, dict) else s.timestamp for s in scores
            )
        timestamps = sorted(list(all_timestamps))
        if not timestamps:
            return

        for topic, scores in all_scores.items():
            scores.sort(
                key=lambda x: x["timestamp"] if isinstance(x, dict) else x.timestamp
            )
            score_dict = {
                (s["timestamp"] if isinstance(s, dict) else s.timestamp): (
                    (s["score"] / s["total"] * 100)
                    if isinstance(s, dict)
                    else (s.score / s.total * 100)
                )
                for s in scores
            }
            percentages = [score_dict.get(ts, None) for ts in timestamps]
            sns.lineplot(
                x=range(len(timestamps)),
                y=percentages,
                ax=ax,
                marker="o",
                label=topic.replace("_", " ").title(),
                linewidth=2,
            )

        ax.set_title("Score Progression by Topic", fontsize=12, weight="bold")
        ax.set_xlabel("Quiz Attempts", fontsize=10)
        ax.set_ylabel("Score (%)", fontsize=10)
        ax.set_xticks(range(len(timestamps)))
        ax.set_xticklabels(
            [ts.strftime("%Y-%m-%d %H:%M") for ts in timestamps], rotation=45
        )
        ax.set_ylim(0, 100)
        ax.legend(title="Topics")

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        self.canvas = canvas

    def back(self):
        self.app.clear_frame()
        self.app.current_frame = self.parent_frame
        self.app.current_frame.pack(fill="both", expand=True)
