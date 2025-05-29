import os
import json
import random
from typing import Optional, List, Dict
from datetime import datetime
import uuid
from tkinter import messagebox
from schemas import (
    QuizConfig,
    Quiz,
    Question,
    Result,
    User,
    Score,
    Users,
    UserCredentials,
)


class DataManager:
    """Handles JSON file operations and data validation."""

    def __init__(self):
        self.config_path = os.path.join(os.path.curdir, "config", "config.json")
        self.data_dir = os.path.join(os.path.curdir, "data")
        self.scores_path = os.path.join(os.path.curdir, "result", "scores.json")
        self.users_path = os.path.join(os.path.curdir, "users", "users.json")

    def load_json_file(self, file_path: str) -> Optional[dict]:
        try:
            if not os.path.exists(file_path):
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "w") as file:
                    json.dump({}, file)
                return {}
            with open(file_path, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            messagebox.showerror("Error", f"Invalid JSON format in {file_path}")
            return None
        except Exception as e:
            messagebox.showerror("Error", f"Error loading {file_path}: {str(e)}")
            return None

    def save_json_file(self, file_path: str, data: dict) -> bool:
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error saving {file_path}: {str(e)}")
            return False

    def load_config(self) -> Optional[QuizConfig]:
        config_data = self.load_json_file(self.config_path)
        if not config_data:
            return None
        try:
            return QuizConfig.model_validate(config_data)
        except Exception as e:
            messagebox.showerror("Error", f"Invalid configuration format: {str(e)}")
            return None

    def load_questions(self, topic: str) -> Optional[List[Question]]:
        path = os.path.join(self.data_dir, f"{topic}.json")
        quiz_raw = self.load_json_file(path)
        if quiz_raw is None:
            return None
        try:
            quiz = Quiz.model_validate(quiz_raw)
            questions = list(quiz.root.values())
            random.shuffle(questions)
            return questions
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error processing questions for {topic}: {str(e)}"
            )
            return None

    def save_question(self, topic: str, question: Question) -> Optional[str]:
        path = os.path.join(self.data_dir, f"{topic}.json")
        quiz_data = self.load_json_file(path)
        if quiz_data is None:
            return None
        try:
            quiz = Quiz.model_validate(quiz_data)
            config = self.load_config()
            if config and len(quiz.root) >= config.questionsPerTopic:
                messagebox.showerror(
                    "Error",
                    f"Topic '{topic}' has reached the limit of {config.questionsPerTopic} questions",
                )
                return None
            question_id = str(uuid.uuid4())
            quiz.root[question_id] = question
            if self.save_json_file(path, quiz.model_dump()):
                return question_id
            return None
        except Exception as e:
            messagebox.showerror("Error", f"Error saving question: {str(e)}")
            return None

    def delete_question(self, topic: str, question_id: str) -> bool:
        path = os.path.join(self.data_dir, f"{topic}.json")
        quiz_data = self.load_json_file(path)
        if quiz_data is None:
            return False
        try:
            quiz = Quiz.model_validate(quiz_data)
            if question_id not in quiz.root:
                messagebox.showerror("Error", f"Question ID '{question_id}' not found")
                return False
            del quiz.root[question_id]
            return self.save_json_file(path, quiz.model_dump())
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting question: {str(e)}")
            return False

    def load_users(self) -> Optional[Users]:
        users_data = self.load_json_file(self.users_path)
        if users_data is None:
            return None
        try:
            return Users.model_validate(users_data)
        except Exception as e:
            messagebox.showerror("Error", f"Invalid users data format: {str(e)}")
            return None

    def save_user(self, user: UserCredentials) -> bool:
        users_data = self.load_json_file(self.users_path)
        if users_data is None:
            return False
        try:
            users = Users.model_validate(users_data)
            if user.username in users.root:
                messagebox.showerror("Error", "Username already exists")
                return False
            users.root[user.username] = user
            return self.save_json_file(self.users_path, users.model_dump())
        except Exception as e:
            messagebox.showerror("Error", f"Error saving user: {str(e)}")
            return False

    def save_score(self, username: str, topic: str, score: int, total: int) -> bool:
        result_data = self.load_json_file(self.scores_path)
        result = (
            Result(root={}) if not result_data else Result.model_validate(result_data)
        )
        if username not in result.root:
            result.root[username] = User(root={})
        if topic not in result.root[username].root:
            result.root[username].root[topic] = []
        new_score = Score(
            timestamp=datetime.now().isoformat(), score=score, total=total
        )
        result.root[username].root[topic].append(new_score)
        return self.save_json_file(self.scores_path, result.model_dump())

    def get_leaderboard(self, topic: str) -> List[Dict]:
        result_data = self.load_json_file(self.scores_path)
        if not result_data:
            return []
        try:
            result = Result.model_validate(result_data)
            leaderboard = []
            for username, user_data in result.root.items():
                if topic in user_data.root:
                    best_score = max(
                        user_data.root[topic],
                        key=lambda x: x.score / x.total if x.total > 0 else 0,
                        default=None,
                    )
                    if best_score:
                        leaderboard.append(
                            {
                                "username": username,
                                "score": best_score.score,
                                "total": best_score.total,
                                "percentage": (
                                    (best_score.score / best_score.total * 100)
                                    if best_score.total > 0
                                    else 0
                                ),
                            }
                        )
            return sorted(leaderboard, key=lambda x: x["percentage"], reverse=True)
        except Exception as e:
            messagebox.showerror("Error", f"Error processing leaderboard: {str(e)}")
            return []

    def get_analytics(self) -> Dict:
        result_data = self.load_json_file(self.scores_path)
        users_data = self.load_json_file(self.users_path)
        config = self.load_config()
        analytics = {
            "total_users": 0,
            "total_topics": len(config.topics) if config else 0,
            "users_took_quizzes": 0,
            "per_topic_activity": {},
        }
        if users_data:
            analytics["total_users"] = len(users_data)
        if result_data:
            try:
                result = Result.model_validate(result_data)
                analytics["users_took_quizzes"] = len(result.root)
                for topic in config.topics if config else []:
                    count = sum(
                        1 for user in result.root.values() if topic in user.root
                    )
                    analytics["per_topic_activity"][topic] = count
            except Exception as e:
                messagebox.showerror("Error", f"Error processing analytics: {str(e)}")
        return analytics

    def get_user_scores(self, username: str) -> dict:
        result_data = self.load_json_file(self.scores_path)
        if not result_data:
            return {}
        try:
            result = Result.model_validate(result_data)
            user_scores = result.root.get(username, None)
            if user_scores:
                return user_scores.root
            return {}
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error retrieving scores for {username}: {str(e)}"
            )
            return {}
