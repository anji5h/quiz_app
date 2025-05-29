import tkinter as tk
import bcrypt
from data_manager import DataManager
from frames.auth_frame import AuthFrame
from schemas import UserCredentials


class QuizApp:
    """Main application class managing Tkinter GUI and logic."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Quiz Application")
        self.root.geometry("800x600")
        self.data_manager = DataManager()
        self.current_user = None
        self.current_frame = None
        self.frames = {}
        self.show_auth_frame()

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.pack_forget()
        self.current_frame = None

    def show_auth_frame(self):
        if "auth" not in self.frames:
            self.frames["auth"] = AuthFrame(self.root, self)
        self.clear_frame()
        self.current_frame = self.frames["auth"]
        self.current_frame.pack(fill="both", expand=True)

    def show_user_frame(self):
        from frames.user_frame import UserFrame

        if "user" not in self.frames:
            self.frames["user"] = UserFrame(self.root, self)
        self.clear_frame()
        self.current_frame = self.frames["user"]
        self.current_frame.pack(fill="both", expand=True)

    def show_admin_frame(self):
        from frames.admin_frame import AdminFrame

        if "admin" not in self.frames:
            self.frames["admin"] = AdminFrame(self.root, self)
        self.clear_frame()
        self.current_frame = self.frames["admin"]
        self.current_frame.pack(fill="both", expand=True)

    def login(self, username: str, password: str) -> bool:
        users = self.data_manager.load_users()
        if not users or username not in users.root:
            tk.messagebox.showerror("Error", "Invalid username or password")
            return False
        user = users.root[username]
        if not bcrypt.checkpw(password.encode(), user.password.encode()):
            tk.messagebox.showerror("Error", "Invalid username or password")
            return False
        self.current_user = user
        if user.role == "ADMIN":
            self.show_admin_frame()
        else:
            self.show_user_frame()
        return True

    def register(self, username: str, password: str) -> bool:
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = UserCredentials(username=username, password=hashed_password, role="USER")
        return self.data_manager.save_user(user)


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
