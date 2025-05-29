import tkinter as tk
from tkinter import messagebox, ttk
from schemas import Question


class AddQuestionFrame(tk.Frame):
    """Frame for adding a new question."""

    def __init__(self, parent, app, parent_frame):
        super().__init__(parent)
        self.app = app
        self.parent_frame = parent_frame
        self.configure(bg="#f0f0f0")
        self.setup_ui()

    def setup_ui(self):
        self.pack(fill="both", expand=True)

        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True)

        # Title
        tk.Label(
            main_frame,
            text="Add Question",
            font=("Arial", 24, "bold"),
            bg="#f0f0f0",
            fg="#333333",
        ).grid(row=0, column=0, columnspan=2, pady=(20, 20), sticky="n")

        # Topic Selection
        tk.Label(
            main_frame,
            text="Topic:",
            font=("Arial", 12),
            bg="#f0f0f0",
            fg="#333333",
            anchor="e",
        ).grid(row=1, column=0, padx=(20, 10), pady=5, sticky="e")
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
        topic_combo.grid(row=1, column=1, padx=(0, 20), pady=5, sticky="w")

        # Question Text
        tk.Label(
            main_frame,
            text="Question Text:",
            font=("Arial", 12),
            bg="#f0f0f0",
            fg="#333333",
            anchor="e",
        ).grid(row=2, column=0, padx=(20, 10), pady=5, sticky="e")
        self.question_entry = tk.Entry(main_frame, width=40, font=("Arial", 12))
        self.question_entry.grid(row=2, column=1, padx=(0, 20), pady=5, sticky="w")

        # Options
        self.option_entries = {}
        for i in range(1, 5):
            tk.Label(
                main_frame,
                text=f"Option {i}:",
                font=("Arial", 12),
                bg="#f0f0f0",
                fg="#333333",
                anchor="e",
            ).grid(row=i + 2, column=0, padx=(20, 10), pady=5, sticky="e")
            self.option_entries[str(i)] = tk.Entry(
                main_frame, width=40, font=("Arial", 12)
            )
            self.option_entries[str(i)].grid(
                row=i + 2, column=1, padx=(0, 20), pady=5, sticky="w"
            )

        tk.Label(
            main_frame,
            text="Correct Answer:",
            font=("Arial", 12),
            bg="#f0f0f0",
            fg="#333333",
            anchor="e",
        ).grid(row=7, column=0, padx=(20, 10), pady=5, sticky="e")
        self.answer_var = tk.StringVar(value="1")
        answer_combo = ttk.Combobox(
            main_frame,
            textvariable=self.answer_var,
            values=["1", "2", "3", "4"],
            state="readonly",
            width=10,
            font=("Arial", 12),
        )
        answer_combo.grid(row=7, column=1, padx=(0, 20), pady=5, sticky="w")

        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.grid(row=8, column=0, columnspan=2, pady=20)
        save_button = tk.Button(
            button_frame,
            text="Save Question",
            command=self.save_question,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            padx=10,
            pady=5,
        )
        save_button.pack(side="left", padx=10)
        back_button = tk.Button(
            button_frame,
            text="Back",
            command=self.back,
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            padx=10,
            pady=5,
        )
        back_button.pack(side="left", padx=10)

    def save_question(self):
        topic = self.topic_var.get().lower().replace(" ", "_")
        question_text = self.question_entry.get().strip()
        options = {k: v.get().strip() for k, v in self.option_entries.items()}
        answer = self.answer_var.get().strip()
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
