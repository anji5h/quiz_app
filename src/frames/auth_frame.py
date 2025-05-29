import tkinter as tk
from tkinter import messagebox


class AuthFrame(tk.Frame):
    """Frame for login and registration."""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self, text="Quiz Application", font=("Arial", 20)).pack(pady=20)
        tk.Label(self, text="Username").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)
        tk.Label(self, text="Password").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)
        tk.Button(self, text="Login", command=self.login).pack(pady=10)
        tk.Button(self, text="Register", command=self.register).pack(pady=5)

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
