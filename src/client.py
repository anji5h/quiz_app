import json
import os
import random
from typing import Optional
from datetime import datetime
from schemas import Question, Quiz, QuizConfig, Result, Score, User

DATA_DIR = os.path.join(os.getcwd(), "data")
CONFIG_FILE_PATH = os.path.join(os.getcwd(), "config", "config.json")
RESULT_FILE_PATH = os.path.join(os.getcwd(), "result", "result.json")


def load_json_file(file_path: str) -> Optional[dict]:
    """Load and parse JSON file, creating an empty file if it doesn't exist."""
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        # File doesn't exist, create one with empty dict
        with open(file_path, "w") as file:
            json.dump({}, file)
        return {}
    except Exception as e:
        print(f"Error loading {file_path}: {str(e)}")
        return None


def save_json_file(file_path: str, data: dict) -> bool:
    """Save data to JSON file with proper formatting."""
    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        return True
    except Exception as e:
        print(f"Error saving {file_path}: {str(e)}")
        return False


def get_username():
    return input("Enter your name: ").strip()


def choose_topic(topics: list[str]) -> str:
    """Display available quiz topics with numbering."""
    if not topics:
        print("No topics available.")
        return

    print("\nAvailable topics for the quiz:")
    for i, topic in enumerate(topics, 1):
        print(f"{i}. {topic.replace("_", " ")}")

    choice = int(input("Choose a topic number of your interest: "))
    return topics[choice - 1]


def load_questions(topic) -> list[Question]:
    path = os.path.join(DATA_DIR, f"{topic}.json")
    quiz_raw = load_json_file(path)

    if quiz_raw is None:
        return

    quiz = Quiz.model_validate(quiz_raw)
    questions = list(quiz.root.values())

    random.shuffle(questions)

    return questions


def ask_questions(questions: list[Question]):
    score = 0
    for idx, q in enumerate(questions, 1):
        print(f"\nQ{idx}: {q.question}")
        for key in q.options:
            print(f"  {key}. {q.options[key]}")
        answer = input("Your answer (1-4): ").strip()
        if q.answer == answer:
            print("✅ Correct!")
            score += 1
        else:
            print(f"❌ Wrong! Correct answer: {q.options[q.answer]}")
    return score


def save_result(username, topic, score, total):
    result_raw = load_json_file(RESULT_FILE_PATH)

    if not result_raw:
        result = Result(root={})
    else:
        result = Result.model_validate(result_raw)

    if username not in result.root:
        result.root[username] = User(root={})

    if topic not in result.root[username].root:
        result.root[username].root[topic] = []

    new_score = Score(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), score=score, total=total
    )

    result.root[username].root[topic].append(new_score)

    save_json_file(RESULT_FILE_PATH, result.model_dump())

    print(f"\n📁 User {username} score saved")


def main():
    print("🎓 Welcome to the Quiz App 🎓")

    config_data = load_json_file(CONFIG_FILE_PATH)
    if not config_data:
        return

    try:
        config = QuizConfig.model_validate(config_data)
    except Exception as e:
        print(f"Invalid configuration: {str(e)}")
        return

    username = get_username()
    topic = choose_topic(config.topics)
    questions = load_questions(topic)
    score = ask_questions(questions)

    print(
        f"\n🏁 {username}, your final score for your chosen topic '{topic}' is: {score}/{len(questions)}"
    )
    save_result(username, topic, score, len(questions))


if __name__ == "__main__":
    main()
