import tkinter as tk
from tkinter import messagebox, ttk
from schemas import Question


class AddQuestionFrame(tk.Frame):
    """Frame for adding a new question."""

    def __init__(self, parent, app, parent_frame):
        super().__init__(parent)
        self.app = app
        self.parent_frame = parent_frame
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self, text="Add Question", font=("Arial", 16)).pack(pady=10)
        tk.Label(self, text="Topic").pack()
        config = self.app.data_manager.load_config()
        self.topic_var = tk.StringVar()
        ttk.Combobox(
            self,
            textvariable=self.topic_var,
            values=[t.replace("_", " ").title() for t in config.topics],
            state="readonly",
        ).pack(pady=5)
        tk.Label(self, text="Question Text").pack()
        self.question_entry = tk.Entry(self, width=50)
        self.question_entry.pack(pady=5)
        self.option_entries = {}
        for i in range(1, 5):
            tk.Label(self, text=f"Option {i}").pack()
            self.option_entries[str(i)] = tk.Entry(self, width=50)
            self.option_entries[str(i)].pack(pady=5)
        tk.Label(self, text="Correct Answer (1-4)").pack()
        self.answer_entry = tk.Entry(self)
        self.answer_entry.pack(pady=5)
        tk.Button(self, text="Save Question", command=self.save_question).pack(pady=10)
        tk.Button(self, text="Back", command=self.back).pack(pady=5)

    def save_question(self):
        topic = self.topic_var.get().lower().replace(" ", "_")
        question_text = self.question_entry.get().strip()
        options = {k: v.get().strip() for k, v in self.option_entries.items()}
        answer = self.answer_entry.get().strip()
        if not topic or not question_text or not all(options.values()) or not answer:
            messagebox.showerror("Error", "All fields must be filled")
            return
        try:
            question = Question(question=question_text, options=options, answer=answer)
            question_id = self.app.data_manager.save_question(topic, question)
            if question_id:
                messagebox.showinfo("Success", f"Question added with ID: {question_id}")
                self.back()
        except Exception as e:
            messagebox.showerror("Error", f"Invalid question data: {str(e)}")

    def back(self):
        self.app.clear_frame()
        self.app.current_frame = self.parent_frame
        self.app.current_frame.pack(fill="both", expand=True)
