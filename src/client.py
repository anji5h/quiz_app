import json
import os
import random
from typing import Optional, List
from datetime import datetime
from schemas import Question, Quiz, QuizConfig, Result, Score, User

# Constants for file paths
DATA_DIR = os.path.join(os.getcwd(), "data")
CONFIG_FILE_PATH = os.path.join(os.getcwd(), "config", "config.json")
RESULT_FILE_PATH = os.path.join(os.getcwd(), "result", "result.json")


def load_json_file(file_path: str) -> Optional[dict]:
    """Load and parse a JSON file, creating an empty file if it doesn't exist.

    Args:
        file_path (str): Path to the JSON file to load.

    Returns:
        Optional[dict]: The parsed JSON data as a dictionary, or None if loading fails.

    Notes:
        - Creates the parent directory and an empty JSON file if it doesn't exist.
        - Handles JSON decode errors and other exceptions with appropriate error messages.
        - If the file is not found, creates an empty JSON file with {}.
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


def get_username() -> str:
    """Get a valid username from user input.

    Returns:
        str: A non-empty username provided by the user.

    Notes:
        - Prompts the user for input in a loop until a non-empty username is provided.
        - Strips whitespace from the input.
    """
    while True:
        username = input("Enter your name: ").strip()
        if username:
            return username
        print("Error: Username cannot be empty")


def choose_topic(topics: List[str]) -> Optional[str]:
    """Display available quiz topics and get user selection.

    Args:
        topics (List[str]): List of topic names from the configuration.

    Returns:
        Optional[str]: Selected topic name, or None if no topics are available or input is invalid.

    Notes:
        - Displays topics with numbering and title case (e.g., 'python_quiz' → 'Python Quiz').
        - Validates user input to ensure it's a valid number within the topic range.
        - Returns None if the topic list is empty or input is invalid after validation.
    """
    if not topics:
        print("Error: No topics available")
        return None

    print("\nAvailable topics for the quiz:")
    # Display topics with numbering
    for i, topic in enumerate(topics, 1):
        print(f"{i}. {topic.replace('_', ' ').title()}")

    while True:
        try:
            # Prompt for topic number
            choice = int(input("Choose a topic number: "))
            if 1 <= choice <= len(topics):
                return topics[choice - 1]
            print(f"Error: Please choose a number between 1 and {len(topics)}")
        except ValueError:
            print("Error: Please enter a valid number")


def load_questions(topic: str) -> Optional[List[Question]]:
    """Load and shuffle questions for the selected topic.

    Args:
        topic (str): Name of the topic to load questions for.

    Returns:
        Optional[List[Question]]: List of shuffled Question objects, or None if loading or validation fails.

    Notes:
        - Loads the topic's JSON file from the data directory.
        - Validates the JSON data against the Quiz schema.
        - Shuffles questions randomly to vary the quiz order.
        - Prints error messages for file or validation issues.
    """
    # Construct path to topic's question file
    path = os.path.join(DATA_DIR, f"{topic}.json")
    quiz_raw = load_json_file(path)

    if quiz_raw is None:
        print(f"Error: Failed to load questions for topic {topic}")
        return None

    try:
        # Validate JSON data against Quiz schema
        quiz = Quiz.model_validate(quiz_raw)
        # Convert question dictionary to list
        questions = list(quiz.root.values())
        # Shuffle questions for random order
        random.shuffle(questions)
        return questions
    except Exception as e:
        print(f"Error processing questions: {str(e)}")
        return None


def ask_questions(questions: List[Question]) -> int:
    """Present questions to the user and calculate their score.

    Args:
        questions (List[Question]): List of Question objects to present.

    Returns:
        int: Number of correct answers (score).

    Notes:
        - Displays each question with numbered options in sorted order.
        - Validates user answers to ensure they are valid option keys (1-4).
        - Provides feedback (correct/wrong) with the correct answer if wrong.
        - Increments score for correct answers.
    """
    score = 0
    for idx, question in enumerate(questions, 1):
        print(f"\nQuestion {idx}: {question.question}")
        # Sort options for consistent display
        for key in sorted(question.options.keys()):
            print(f"  {key}. {question.options[key]}")
        
        # Prompt for answer with validation
        while True:
            answer = input("Your answer (1-4): ").strip()
            if answer in question.options:
                break
            print("Error: Please enter a number between 1 and 4")

        # Check answer and provide feedback
        if answer == question.answer:
            print("✅ Correct!")
            score += 1
        else:
            print(f"❌ Wrong! Correct answer: {question.options[question.answer]}")
    return score


def save_result(username: str, topic: str, score: int, total: int) -> None:
    """Save quiz results to the result file.

    Args:
        username (str): User's name.
        topic (str): Name of the quiz topic.
        score (int): Number of correct answers.
        total (int): Total number of questions.

    Notes:
        - Loads existing result data or initializes an empty Result object.
        - Structures results as a nested dictionary: users → topics → scores.
        - Adds a new Score object with timestamp, score, and total.
        - Saves the updated results to the result file.
    """
    # Load existing results or initialize empty
    result_raw = load_json_file(RESULT_FILE_PATH)
    result = Result(root={}) if not result_raw else Result.model_validate(result_raw)

    # Initialize user if not present
    if username not in result.root:
        result.root[username] = User(root={})

    # Initialize topic for user if not present
    if topic not in result.root[username].root:
        result.root[username].root[topic] = []

    # Create new score entry
    new_score = Score(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        score=score,
        total=total
    )
    # Append score to user's topic results
    result.root[username].root[topic].append(new_score)

    # Save updated results
    if save_json_file(RESULT_FILE_PATH, result.model_dump()):
        print(f"\n📁 Score saved for user {username}")
    else:
        print(f"\n⚠️ Failed to save score for user {username}")


def main() -> None:
    """Run the quiz application.

    Notes:
        - Loads configuration and exits if invalid.
        - Prompts for username and topic selection.
        - Loads and presents questions, calculates score, and saves results.
        - Handles early exits if configuration, topic, or questions are invalid.
    """
    print("🎓 Welcome to the Quiz App 🎓")

    # Load and validate configuration
    config = load_config()
    if not config:
        return

    # Get username with validation
    username = get_username()
    # Select topic with validation
    topic = choose_topic(config.topics)
    if not topic:
        return

    # Load questions for the topic
    questions = load_questions(topic)
    if not questions:
        return

    # Run quiz and get score
    score = ask_questions(questions)
    # Display final score
    print(f"\n🏁 {username}, your score for '{topic.replace('_', ' ').title()}' is: {score}/{len(questions)}")
    # Save results
    save_result(username, topic, score, len(questions))


if __name__ == "__main__":
    main()