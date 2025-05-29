import tkinter as tk
from tkinter import messagebox

class AuthFrame(tk.Frame):
    """Frame for login and registration."""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.configure(bg="#f0f0f0")
        self.setup_ui()

    def setup_ui(self):
        self.pack(fill="both", expand=True)

        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.pack(expand=True)

        # Title
        title_label = tk.Label(
            main_frame,
            text="Quiz Application",
            font=("Arial", 24, "bold"),
            bg="#f0f0f0",
            fg="#333333",
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(20, 20), sticky="n")

        # Username
        username_label = tk.Label(
            main_frame,
            text="Username:",
            font=("Arial", 12),
            bg="#f0f0f0",
            fg="#333333",
            anchor="w",
        )
        username_label.grid(row=1, column=0, padx=(20, 0), pady=(5, 0), sticky="w")
        self.username_entry = tk.Entry(main_frame, width=30, font=("Arial", 12))
        self.username_entry.grid(row=2, column=0, padx=(20, 0), pady=(0, 10), sticky="w")

        # Password
        password_label = tk.Label(
            main_frame,
            text="Password:",
            font=("Arial", 12),
            bg="#f0f0f0",
            fg="#333333",
            anchor="w",
        )
        password_label.grid(row=3, column=0, padx=(20, 0), pady=(5, 0), sticky="w")
        self.password_entry = tk.Entry(
            main_frame, show="*", width=30, font=("Arial", 12)
        )
        self.password_entry.grid(row=4, column=0, padx=(20, 0), pady=(0, 10), sticky="w")

        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        login_button = tk.Button(
            button_frame,
            text="Login",
            command=self.login,
            font=("Arial", 12),
            padx=10,
            pady=5,
        )
        login_button.pack(side="left", padx=10)
        register_button = tk.Button(
            button_frame,
            text="Register",
            command=self.register,
            font=("Arial", 12),
            padx=10,
            pady=5,
        )
        register_button.pack(side="left", padx=10)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty")
            return
        self.app.login(username, password)

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty")
            return
        if self.app.register(username, password):
            messagebox.showinfo("Success", "Registration successful! Please login.")
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)