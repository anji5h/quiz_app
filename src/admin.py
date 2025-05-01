import json
import os
import uuid
from typing import Optional, List
from schemas import QuizConfig, Quiz, Question

# Constants for file paths
CONFIG_FILE_PATH = os.path.join(os.getcwd(), "config", "config.json")
DATA_DIR = os.path.join(os.getcwd(), "data")


def load_json_file(file_path: str) -> Optional[dict]:
    """Load and parse a JSON file, creating an empty file if it doesn't exist.

    Args:
        file_path (str): Path to the JSON file to load.

    Returns:
        Optional[dict]: The parsed JSON data as a dictionary, or None if loading fails.

    Notes:
        - Creates the parent directory and an empty JSON file if it doesn't exist.
        - Handles JSON decode errors and other exceptions with appropriate error messages - If the file is not found, creates an empty JSON file with {}.
    """
    try:
        # Check if file exists; if not, create directory and empty file
        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as file:
                json.dump({}, file)
            return {}
        
        # Read and parse the JSON file
        with open(file_path, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}")
        return None
    except Exception as e:
        print(f"Error loading {file_path}: {str(e)}")
        return None


def save_json_file(file_path: str, data: dict) -> bool:
    """Save data to a JSON file with proper formatting.

    Args:
        file_path (str): Path to the JSON file to save.
        data (dict): Data to save as JSON.

    Returns:
        bool: True if saving was successful, False otherwise.

    Notes:
        - Creates the parent directory if it doesn't exist.
        - Formats JSON with indentation for readability.
    """
    try:
        # Ensure the parent directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # Write data to file with indentation
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        return True
    except Exception as e:
        print(f"Error saving {file_path}: {str(e)}")
        return False


def load_config() -> Optional[QuizConfig]:
    """Load and validate the quiz configuration from the config file.

    Returns:
        Optional[QuizConfig]: Validated QuizConfig object, or None if loading or validation fails.

    Notes:
        - Uses load_json_file to read the config file.
        - Validates the JSON data against the QuizConfig schema.
        - Prints specific error messages for JSON or validation failures.
    """
    config_data = load_json_file(CONFIG_FILE_PATH)
    if not config_data:
        print("Error: Failed to load configuration")
        return None
    
    try:
        # Validate JSON data against QuizConfig schema
        return QuizConfig.model_validate(config_data)
    except Exception as e:
        print(f"Error: Invalid configuration format: {str(e)}")
        return None


def print_topics(topics: List[str]) -> None:
    """Display available quiz topics with numbering.

    Args:
        topics (List[str]): List of topic names.

    Notes:
        - Formats topic names by replacing underscores with spaces and applying title case.
        - Prints numbered list of topics or an error if the list is empty.
    """
    if not topics:
        print("Error: No topics available")
        return
    print("\nAvailable Quiz Topics:")
    # Iterate with index for numbered list
    for idx, topic in enumerate(topics, 1):
        print(f"{idx}. {topic.replace('_', ' ').title()}")


def validate_option(option: str) -> bool:
    """Validate if the option is one of 1, 2, 3, or 4.

    Args:
        option (str): The option to validate.

    Returns:
        bool: True if the option is valid (1, 2, 3, or 4), False otherwise.

    Notes:
        - Case-insensitive comparison.
    """
    return option.lower() in {"1", "2", "3", "4"}


def add_question(ques_per_topic: int, topic_name: str) -> None:
    """Add a new question to the specified topic.

    Args:
        ques_per_topic (int): Maximum number of questions allowed per topic.
        topic_name (str): Name of the topic to add the question to.

    Notes:
        - Loads the existing quiz data for the topic.
        - Checks if the topic has reached the question limit.
        - Prompts for question text, options, and correct answer with validation.
        - Saves the updated quiz data with a new UUID for the question.
    """
    quiz_file_path = os.path.join(DATA_DIR, f"{topic_name}.json")
    quiz_data = load_json_file(quiz_file_path)

    if quiz_data is None:
        print(f"Error: Failed to load quiz data for topic '{topic_name}'")
        return

    try:
        # Validate quiz data against Quiz schema
        quiz = Quiz.model_validate(quiz_data)
    except Exception as e:
        print(f"Error: Invalid quiz data format for '{topic_name}': {str(e)}")
        return

    # Check if topic has reached question limit
    if len(quiz.root) >= ques_per_topic:
        print(f"Error: '{topic_name}' has reached the limit of {ques_per_topic} questions")
        return

    # Prompt for question text with validation
    while True:
        ques = input("\nEnter question text (non-empty): ").strip()
        if ques:
            break
        print("Error: Question cannot be empty")

    # Prompt for four options with validation
    options = {}
    for opt in ["1", "2", "3", "4"]:
        while True:
            option_text = input(f"Enter option {opt} (non-empty): ").strip()
            if option_text:
                options[opt] = option_text
                break
            print(f"Error: Option {opt} cannot be empty")

    # Prompt for correct answer with validation
    while True:
        ans = input("Enter correct option (1, 2, 3, or 4): ").strip()
        if validate_option(ans):
            break
        print("Error: Invalid answer. Must be 1, 2, 3, or 4")

    # Create new question object with validated data
    new_question = Question(
        question=ques,
        options=options,
        answer=ans,
    )
    # Generate unique ID for the question
    ques_id = str(uuid.uuid4())
    quiz.root[ques_id] = new_question

    # Save updated quiz data
    if save_json_file(quiz_file_path, quiz.model_dump()):
        print(f"✅ Question added successfully with ID: {ques_id}")
    else:
        print(f"⚠️ Failed to save question")


def delete_question(topic_name: str, ques_id: str) -> None:
    """Delete a question from the specified topic.

    Args:
        topic_name (str): Name of the topic containing the question.
        ques_id (str): ID of the question to delete.

    Notes:
        - Loads the quiz data for the topic.
        - Checks if the question ID exists.
        - Removes the question and saves the updated quiz data.
    """
    quiz_file_path = os.path.join(DATA_DIR, f"{topic_name}.json")
    quiz_data = load_json_file(quiz_file_path)

    if quiz_data is None:
        print(f"Error: Failed to load quiz data for topic '{topic_name}'")
        return

    try:
        # Validate quiz data against Quiz schema
        quiz = Quiz.model_validate(quiz_data)
    except Exception as e:
        print(f"Error: Invalid quiz data format for '{topic_name}': {str(e)}")
        return

    # Check if question ID exists
    if ques_id not in quiz.root:
        print(f"Error: Question with ID '{ques_id}' not found")
        return

    # Remove the question
    del quiz.root[ques_id]

    # Save updated quiz data
    if save_json_file(quiz_file_path, quiz.model_dump()):
        print(f"✅ Question '{ques_id}' deleted successfully")
    else:
        print(f"⚠️ Failed to delete question")


def main() -> None:
    """Main function to manage quiz questions.

    Notes:
        - Loads configuration and validates admin password.
        - Provides a menu to add or delete questions or exit.
        - Handles topic selection and input validation for all operations.
        - Runs in a loop until the user chooses to exit.
    """
    print("🎓 Welcome to the Quiz Management System 🎓")

    # Load and validate configuration
    config = load_config()
    if not config:
        return

    # Prompt for admin password with validation
    while True:
        password = input("Enter admin password: ").strip()
        if password:
            break
        print("Error: Password cannot be empty")

    # Verify password against config
    if password != config.appPassword:
        print("Error: Incorrect password")
        return

    while True:
        # Display menu options
        print("\n=== Quiz Management System ===")
        print("1. Add question to topic")
        print("2. Delete question from topic")
        print("3. Exit")

        # Prompt for menu choice with validation
        choice = input("Enter choice (1-3): ").strip()
        if not choice.isdigit() or int(choice) not in {1, 2, 3}:
            print("Error: Invalid choice. Please enter 1, 2, or 3")
            continue

        choice = int(choice)
        if choice == 3:
            print("Exiting Quiz Management System...")
            break

        # Display available topics
        print_topics(config.topics)
        # Prompt for topic selection with validation
        while True:
            topic_choice = input("Enter topic number: ").strip()
            if topic_choice.isdigit() and 1 <= int(topic_choice) <= len(config.topics):
                break
            print(f"Error: Invalid topic number. Choose between 1 and {len(config.topics)}")

        topic_name = config.topics[int(topic_choice) - 1]

        if choice == 1:
            # Add a new question to the selected topic
            add_question(config.questionsPerTopic, topic_name)
        else:
            # Prompt for question ID with validation
            while True:
                ques_id = input("Enter question ID to delete: ").strip()
                if ques_id:
                    break
                print("Error: Question ID cannot be empty")
            # Delete the specified question
            delete_question(topic_name, ques_id)


if __name__ == "__main__":
    main()