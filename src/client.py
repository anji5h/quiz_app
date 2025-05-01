import json
import os
import random
from typing import Optional, List
from datetime import datetime
from schemas import Question, Quiz, QuizConfig, Result, Score, User

DATA_DIR = os.path.join(os.getcwd(), "data")
CONFIG_FILE_PATH = os.path.join(os.getcwd(), "config", "config.json")
RESULT_FILE_PATH = os.path.join(os.getcwd(), "result", "result.json")


def load_json_file(file_path: str) -> Optional[dict]:
    """Load and parse JSON file, creating an empty file if it doesn't exist."""
    try:
        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as file:
                json.dump({}, file)
            return {}
        
        with open(file_path, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}")
        return None
    except Exception as e:
        print(f"Error loading {file_path}: {str(e)}")
        return None


def save_json_file(file_path: str, data: dict) -> bool:
    """Save data to JSON file with proper formatting."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        return True
    except Exception as e:
        print(f"Error saving {file_path}: {str(e)}")
        return False


def load_config() -> Optional[QuizConfig]:
    """Load and validate quiz configuration from file."""
    config_data = load_json_file(CONFIG_FILE_PATH)
    if not config_data:
        print("Error: Failed to load configuration")
        return None
    
    try:
        return QuizConfig.model_validate(config_data)
    except Exception as e:
        print(f"Error: Invalid configuration format: {str(e)}")
        return None


def get_username() -> str:
    """Get a valid username from user input."""
    while True:
        username = input("Enter your name: ").strip()
        if username:
            return username
        print("Error: Username cannot be empty")


def choose_topic(topics: List[str]) -> Optional[str]:
    """Display available quiz topics and get user selection."""
    if not topics:
        print("Error: No topics available")
        return None

    print("\nAvailable topics for the quiz:")
    for i, topic in enumerate(topics, 1):
        print(f"{i}. {topic.replace('_', ' ').title()}")

    while True:
        try:
            choice = int(input("Choose a topic number: "))
            if 1 <= choice <= len(topics):
                return topics[choice - 1]
            print(f"Error: Please choose a number between 1 and {len(topics)}")
        except ValueError:
            print("Error: Please enter a valid number")


def load_questions(topic: str) -> Optional[List[Question]]:
    """Load and shuffle questions for the selected topic."""
    path = os.path.join(DATA_DIR, f"{topic}.json")
    quiz_raw = load_json_file(path)

    if quiz_raw is None:
        print(f"Error: Failed to load questions for topic {topic}")
        return None

    try:
        quiz = Quiz.model_validate(quiz_raw)
        questions = list(quiz.root.values())
        random.shuffle(questions)
        return questions
    except Exception as e:
        print(f"Error processing questions: {str(e)}")
        return None


def ask_questions(questions: List[Question]) -> int:
    """Present questions to user and calculate score."""
    score = 0
    for idx, question in enumerate(questions, 1):
        print(f"\nQuestion {idx}: {question.question}")
        for key in sorted(question.options.keys()):
            print(f"  {key}. {question.options[key]}")
        
        while True:
            answer = input("Your answer (1-4): ").strip()
            if answer in question.options:
                break
            print("Error: Please enter a number between 1 and 4")

        if answer == question.answer:
            print("✅ Correct!")
            score += 1
        else:
            print(f"❌ Wrong! Correct answer: {question.options[question.answer]}")
    return score


def save_result(username: str, topic: str, score: int, total: int) -> None:
    """Save quiz results to file."""
    result_raw = load_json_file(RESULT_FILE_PATH)
    result = Result(root={}) if not result_raw else Result.model_validate(result_raw)

    if username not in result.root:
        result.root[username] = User(root={})

    if topic not in result.root[username].root:
        result.root[username].root[topic] = []

    new_score = Score(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        score=score,
        total=total
    )
    result.root[username].root[topic].append(new_score)

    if save_json_file(RESULT_FILE_PATH, result.model_dump()):
        print(f"\n📁 Score saved for user {username}")
    else:
        print(f"\n⚠️ Failed to save score for user {username}")


def main() -> None:
    """Run the quiz application."""
    print("🎓 Welcome to the Quiz App 🎓")

    config = load_config()
    if not config:
        return

    username = get_username()
    topic = choose_topic(config.topics)
    if not topic:
        return

    questions = load_questions(topic)
    if not questions:
        return

    score = ask_questions(questions)
    print(f"\n🏁 {username}, your score for '{topic.replace('_', ' ').title()}' is: {score}/{len(questions)}")
    save_result(username, topic, score, len(questions))


if __name__ == "__main__":
    main()