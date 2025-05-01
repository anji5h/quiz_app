import json
import os
import uuid
from schemas import QuizConfig, Quiz, Question
from typing import Optional

CONFIG_FILE_PATH = os.path.join(os.getcwd(), "config", "config.json")
DATA_DIR = os.path.join(os.getcwd(), "data")


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


def print_topics(topics: list[str]) -> None:
    """Display available quiz topics with numbering."""
    if not topics:
        print("No topics available.")
        return
    print("\nAvailable Quiz Topics:")
    for idx, topic in enumerate(topics, 1):
        print(f"{idx}. {topic.replace("_", " ")}")


def validate_option(option: str) -> bool:
    """Validate if the option is one of 1, 2, 3, or 4."""
    return option.lower() in {"1", "2", "3", "4"}


def add_question(ques_per_topic: int, topic_name: str) -> None:
    """Add a new question to the specified topic."""
    quiz_file_path = os.path.join(DATA_DIR, f"{topic_name}.json")
    quiz_data = load_json_file(quiz_file_path)

    if quiz_data is None:
        return

    quiz = Quiz.model_validate(quiz_data)

    # Check if maximum questions reached
    if len(quiz.root) >= ques_per_topic:
        print(
            f"Limit reached: '{topic_name}' can have only {ques_per_topic} questions."
        )
        return

    # Get question details with validation
    ques = input("\nEnter question text (non-empty): ").strip()
    if not ques:
        print("Question cannot be empty.")
        return

    options = {}
    for opt in ["1", "2", "3", "4"]:
        option_text = input(f"Enter option {opt} (non-empty): ").strip()
        if not option_text:
            print(f"Option {opt} cannot be empty.")
            return
        options[opt] = option_text

    ans = input("Enter correct option (1, 2, 3, or 4): ").strip().lower()
    if not validate_option(ans):
        print("Invalid answer. Must be 1, 2, 3, or 4")
        return

    # Create and add new question
    new_question = Question(
        question=ques,
        options=options,
        answer=ans,
    )
    ques_id = str(uuid.uuid4())
    quiz.root[ques_id] = new_question

    # Save updated quiz
    if save_json_file(quiz_file_path, quiz.model_dump()):
        print(f"Question added successfully with ID: {ques_id}")
    else:
        print("Failed to save question.")


def delete_question(topic_name: str, ques_id: str) -> None:
    """Delete a question from the specified topic."""
    quiz_file_path = os.path.join(DATA_DIR, f"{topic_name}.json")
    quiz_data = load_json_file(quiz_file_path)

    if not quiz_data:
        print(f"Topic file '{topic_name}.json' not found.")
        return

    quiz = Quiz.model_validate(quiz_data)

    if ques_id not in quiz.root:
        print(f"Question with id: '{ques_id}' not found.")
        return

    del quiz.root[ques_id]

    if save_json_file(quiz_file_path, quiz.model_dump()):
        print(f"Question '{ques_id}' deleted successfully.")
    else:
        print("Failed to delete question.")


def main():
    """Main function to manage quiz questions."""
    # Load configuration
    config_data = load_json_file(CONFIG_FILE_PATH)
    if not config_data:
        return

    try:
        config = QuizConfig.model_validate(config_data)
    except Exception as e:
        print(f"Invalid configuration: {str(e)}")
        return

    # Validate password
    password = input("Enter admin password: ").strip()
    if not password:
        print("Password cannot be empty.")
        return
    if password != config.appPassword:
        print("Incorrect password.")
        return

    while True:
        print("\n=== Quiz Management System ===")
        print("1. Add question to topic")
        print("2. Delete question from topic")
        print("3. Exit")

        choice = input("Enter choice (1-3): ").strip()
        if not choice.isdigit() or int(choice) not in {1, 2, 3}:
            print("Invalid choice. Please enter 1, 2, or 3.")
            continue

        choice = int(choice)
        if choice == 3:
            print("Exiting Quiz Management System...")
            break

        print_topics(config.topics)
        topic_choice = input("Enter topic number: ").strip()

        if not topic_choice.isdigit() or not (
            1 <= int(topic_choice) <= len(config.topics)
        ):
            print("Invalid topic number.")
            continue

        topic_name = config.topics[int(topic_choice) - 1]

        if choice == 1:
            add_question(config.questionsPerTopic, topic_name)
        else:
            ques_id = input("Enter question ID to delete: ").strip()
            if not ques_id:
                print("Question ID cannot be empty.")
                continue
            delete_question(topic_name, ques_id)


if __name__ == "__main__":
    main()
