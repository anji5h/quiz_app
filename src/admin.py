import json
import os
from schemas import QuizConfig

CONFIG_DIR = "src/static"
QUIZ_CONFIG_FILE_PATH = os.path.join(CONFIG_DIR, "admin.json")
QUESTION_FILE_PATH = os.path.join(CONFIG_DIR, "questions.json")

def print_topics(topics: list[str]):
    print("Select the quiz topic: ")
    for idx, topic in enumerate(topics, 1):
        print(f"Topic {idx}: {topic}")

def main():
    try:
        with open(QUIZ_CONFIG_FILE_PATH, "r") as file:
            raw_config = json.load(file)

        quiz_config = QuizConfig(**raw_config)

        password = input("Enter app password: ").strip()

        if password != quiz_config.appPassword:
            print("Wrong password")
            return
        
        while True:
            print("Select a task below:")
            print("Task-1: Add a question to topic")
            print("Task-2: Delete a question of topic")
            print("Task-3: Exit the program")
            task = int(input("Enter the task number: ").strip())

            match task:
                case 1:
                    print_topics(quiz_config.categories)
                    topic_no = int(input("Enter the topic number: ").strip())
                    topic = quiz_config.categories[topic_no - 1]

                    question = input("Enter your question: ")
                    option_a = input("Enter first option (a): ")
                    option_b = input("Enter second option (b): ")
                    option_c = input("Enter third option (c): ")
                    option_d = input("Enter fourth option (d): ")
                    answer = input("Enter correct option (a, b, c, d): ")
                case 2:
                    print_topics(quiz_config.categories)
                    topic_no = int(input("Enter the topic number: ").strip())
                    topic = quiz_config.categories[topic_no - 1]
                case _:
                    break

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
