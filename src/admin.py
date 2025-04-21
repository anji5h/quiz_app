import json
import os
import uuid
from schemas import QuizConfig, Quiz, Question, Topic

CONFIG_DIR = "src/static"
ADMIN_FILE_PATH = os.path.join(CONFIG_DIR, "admin.json")
QUIZ_FILE_PATH = os.path.join(CONFIG_DIR, "quiz.json")


def print_topics(topics: list[str]):
    print("\nSelect the quiz topic: ")
    for idx, topic in enumerate(topics, 1):
        print(f"Topic {idx}: {topic}")


def add_question(
    ques_per_topic: int,
    topic_name: str,
):
    with open(QUIZ_FILE_PATH, "r") as f:
        raw_data = f.read()
        quiz = Quiz.model_validate_json(raw_data)

    if topic_name not in quiz.root:
        quiz.root[topic_name] = Topic(root={})

    topic = quiz.root[topic_name]

    if len(topic.root) >= ques_per_topic:
        print("Already 10 questions")
        return

    ques = input("\nEnter your question: ")
    opt_a = input("Enter first option (a): ")
    opt_b = input("Enter second option (b): ")
    opt_c = input("Enter third option (c): ")
    opt_d = input("Enter fourth option (d): ")
    ans = input("Enter correct option (a, b, c, d): ")

    new_question = Question(
        question=ques, a=opt_a, b=opt_b, c=opt_c, d=opt_d, answer=ans
    )
    ques_id = str(uuid.uuid4())

    topic.root[ques_id] = new_question

    with open(QUIZ_FILE_PATH, "w") as f:
        json.dump(quiz.model_dump(), f, indent=4)


def delete_question(topic_name: str, ques_id: str):
    with open(QUIZ_FILE_PATH, "r") as file:
        raw_data = file.read()
        quiz = Quiz.model_validate_json(raw_data)

    if topic_name not in quiz.root:
        return

    topic = quiz.root[topic_name]
    removed = topic.root.pop(ques_id, None)

    if removed:
        with open(QUIZ_FILE_PATH, "w") as f:
            json.dump(quiz.model_dump(), f, indent=4)


def main():
    try:
        with open(ADMIN_FILE_PATH, "r") as file:
            raw_data = json.load(file)
            config = QuizConfig(**raw_data)

        password = input("Enter app password: ").strip()

        if password != config.appPassword:
            print("Wrong password")
            return

        while True:
            print("\nSelect a task below:")
            print("Task-1: Add a question to topic")
            print("Task-2: Delete a question of topic")
            print("Task-3: Exit the program")
            task = int(input("Enter the task number: ").strip())

            match task:
                case 1:
                    print_topics(config.categories)
                    topic_no = int(input("Enter the topic number: ").strip())
                    topic_name = config.categories[topic_no - 1]
                    add_question(
                        ques_per_topic=config.questionsPerTopic, topic_name=topic_name
                    )
                case 2:
                    print_topics(config.categories)
                    topic_no = int(input("Enter the topic number: ").strip())
                    topic_name = config.categories[topic_no - 1]
                    ques_id = input("Enter question id to delete: ")
                    delete_question(topic_name=topic_name, ques_id=ques_id)
                case _:
                    print("Exiting the application......")
                    break

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
