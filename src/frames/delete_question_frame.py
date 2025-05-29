import tkinter as tk
from tkinter import ttk, messagebox
import os


class DeleteQuestionFrame(tk.Frame):
    """Frame for deleting a question."""

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
            text="Delete Question",
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
        config = self.app.data_manager.load_config()
        self.topic_var = tk.StringVar()
        topic_combo = ttk.Combobox(
            main_frame,
            textvariable=self.topic_var,
            values=[t.replace("_", " ").title() for t in config.topics],
            state="readonly",
            width=30,
            font=("Arial", 12),
        )
        topic_combo.pack(pady=5)

        # Load Questions Button
        tk.Button(
            main_frame,
            text="Load Questions",
            command=self.load_questions,
            font=("Arial", 10),
            bg="#FF9800",
            fg="white",
            width=10,
            padx=10,
            pady=5,
        ).pack(pady=10)

        # Treeview for questions
        tree_frame = tk.Frame(main_frame, bg="#f0f0f0")
        tree_frame.pack(pady=10, fill="x")
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Question"),
            show="headings",
            style="Treeview",
            height=10,
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("Question", text="Question")
        self.tree.column("ID", anchor="center", width=220)
        self.tree.column("Question", anchor="w", width=450)
        self.tree.pack(fill="x", padx=20)

        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(pady=20)
        tk.Button(
            button_frame,
            text="Delete Selected",
            command=self.delete_question,
            font=("Arial", 12),
            bg="#F44336",
            fg="white",
            width=15,
            padx=10,
            pady=5,
        ).pack(side="left", padx=10)
        tk.Button(
            button_frame,
            text="Back",
            command=self.back,
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            width=15,
            padx=10,
            pady=5,
        ).pack(side="left", padx=10)

    def load_questions(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        topic = self.topic_var.get().lower().replace(" ", "_")
        if not topic:
            messagebox.showerror("Error", "Please select a topic")
            return
        questions = self.app.data_manager.load_questions(topic)
        if questions:
            quiz_data = self.app.data_manager.load_json_file(
                os.path.join(self.app.data_manager.data_dir, f"{topic}.json")
            )
            for qid, q in quiz_data.items():
                self.tree.insert("", tk.END, values=(qid, q["question"]))

    def delete_question(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a question to delete")
            return
        topic = self.topic_var.get().lower().replace(" ", "_")
        qid = self.tree.item(selected[0])["values"][0]
        if self.app.data_manager.delete_question(topic, qid):
            messagebox.showinfo("Success", f"Question {qid} deleted")
            self.load_questions()

    def back(self):
        self.app.clear_frame()
        self.app.current_frame = self.parent_frame
        self.app.current_frame.pack(fill="both", expand=True)
