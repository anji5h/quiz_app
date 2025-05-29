import tkinter as tk
from tkinter import ttk, messagebox
import os


class DeleteQuestionFrame(tk.Frame):
    """Frame for deleting a question."""

    def __init__(self, parent, app, parent_frame):
        super().__init__(parent)
        self.app = app
        self.parent_frame = parent_frame
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self, text="Delete Question", font=("Arial", 16)).pack(pady=10)
        config = self.app.data_manager.load_config()
        tk.Label(self, text="Select Topic").pack()
        self.topic_var = tk.StringVar()
        ttk.Combobox(
            self,
            textvariable=self.topic_var,
            values=[t.replace("_", " ").title() for t in config.topics],
            state="readonly",
        ).pack(pady=5)
        tk.Button(self, text="Load Questions", command=self.load_questions).pack(pady=5)
        tk.Button(self, text="Back", command=self.back).pack(pady=5)
        self.tree = ttk.Treeview(self, columns=("ID", "Question"), show="headings")
        self.tree.heading("ID", text="Question ID")
        self.tree.heading("Question", text="Question Text")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        tk.Button(self, text="Delete Selected", command=self.delete_question).pack(
            pady=5
        )

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
                os.path.join(self.app.data_manager.data_dir, f"quiz_{topic}.json")
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
