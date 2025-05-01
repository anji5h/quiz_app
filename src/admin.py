import json
import os
import uuid
from typing import Optional, List
from schemas import QuizConfig, Quiz, Question

CONFIG_FILE_PATH = os.path.join(os.getcwd(), "config", "config.json")
DATA_DIR = os.path.join(os.getcwd(), "data")

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


def print_topics(topics: List[str]) -> None:
    """Display available quiz topics with numbering."""
    if not topics:
        print("Error: No topics available")
        return
    print("\nAvailable Quiz Topics:")
    for idx, topic in enumerate(topics, 1):
        print(f"{idx}. {topic.replace('_', ' ').title()}")


def validate_option(option: str) -> bool:
    """Validate if the option is one of 1, 2, 3, or 4."""
    return option.lower() in {"1", "2", "3", "4"}


def add_question(ques_per_topic: int, topic_name: str) -> None:
    """Add a new question to the specified topic."""
    quiz_file_path = os.path.join(DATA_DIR, f"{topic_name}.json")
    quiz_data = load_json_file(quiz_file_path)

    if quiz_data is None:
        print(f"Error: Failed to load quiz data for topic '{topic_name}'")
        return

    try:
        quiz = Quiz.model_validate(quiz_data)
    except Exception as e:
        print(f"Error: Invalid quiz data format for '{topic_name}': {str(e)}")
        return

    # Check if maximum questions reached
    if len(quiz.root) >= ques_per_topic:
        print(f"Error: '{topic_name}' has reached the limit of {ques_per_topic} questions")
        return

    # Get question details with validation
    while True:
        ques = input("\nEnter question text (non-empty): ").strip()
        if ques:
            break
        print("Error: Question cannot be empty")

    options = {}
    for opt in ["1", "2", "3", "4"]:
        while True:
            option_text = input(f"Enter option {opt} (non-empty): ").strip()
            if option_text:
                options[opt] = option_text
                break
            print(f"Error: Option {opt} cannot be empty")

    while True:
        ans = input("Enter correct option (1, 2, 3, or 4): ").strip()
        if validate_option(ans):
            break
        print("Error: Invalid answer. Must be 1, 2, 3, or 4")

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
        print(f"✅ Question added successfully with ID: {ques_id}")
    else:
        print(f"⚠️ Failed to save question")


def delete_question(topic_name: str, ques_id: str) -> None:
    """Delete a question from the specified topic."""
    quiz_file_path = os.path.join(DATA_DIR, f"{topic_name}.json")
    quiz_data = load_json_file(quiz_file_path)

    if quiz_data is None:
        print(f"Error: Failed to load quiz data for topic '{topic_name}'")
        return

    try:
        quiz = Quiz.model_validate(quiz_data)
    except Exception as e:
        print(f"Error: Invalid quiz data format for '{topic_name}': {str(e)}")
        return

    if ques_id not in quiz.root:
        print(f"Error: Question with ID '{ques_id}' not found")
        return

    del quiz.root[ques_id]

    if save_json_file(quiz_file_path, quiz.model_dump()):
        print(f"✅ Question '{ques_id}' deleted successfully")
    else:
        print(f"⚠️ Failed to delete question")


def main() -> None:
    """Main function to manage quiz questions."""
    print("🎓 Welcome to the Quiz Management System 🎓")

    # Load configuration
    config = load_config()
    if not config:
        return

    # Validate password
    while True:
        password = input("Enter admin password: ").strip()
        if password:
            break
        print("Error: Password cannot be empty")

    if password != config.appPassword:
        print("Error: Incorrect password")
        return

    while True:
        print("\n=== Quiz Management System ===")
        print("1. Add question to topic")
        print("2. Delete question from topic")
        print("3. Exit")

        choice = input("Enter choice (1-3): ").strip()
        if not choice.isdigit() or int(choice) not in {1, 2, 3}:
            print("Error: Invalid choice. Please enter 1, 2, or 3")
            continue

        choice = int(choice)
        if choice == 3:
            print("Exiting Quiz Management System...")
            break

        print_topics(config.topics)
        while True:
            topic_choice = input("Enter topic number: ").strip()
            if topic_choice.isdigit() and 1 <= int(topic_choice) <= len(config.topics):
                break
            print(f"Error: Invalid topic number. Choose between 1 and {len(config.topics)}")

        topic_name = config.topics[int(topic_choice) - 1]

        if choice == 1:
            add_question(config.questionsPerTopic, topic_name)
        else:
            while True:
                ques_id = input("Enter question ID to delete: ").strip()
                if ques_id:
                    break
                print("Error: Question ID cannot be empty")
            delete_question(topic_name, ques_id)


if __name__ == "__main__":
    main()