# quiz_cli.py

import json
import os
import random

DATA_DIR = os.path(os.getcwd(), "data")
CONFIG_FILE_PATH = os.path(os.getcwd(), "client", "config.json")

def get_username():
    return input("Enter your name: ").strip()

def choose_topic():
    topics = [f.split('.')[0] for f in os.listdir(DATA_DIR) if f.endswith('.json')]
    print("\nAvailable topics for the quiz:")
    for i, topic in enumerate(topics, 1):
        print(f"{i}. {topic}")
    
    choice = int(input("Choose a topic number of your interest: "))
    return topics[choice - 1]

def load_questions(topic):
    path = f"{DATA_DIR}/{topic}.json"
    with open(path, 'r') as file:
        questions = json.load(file)

    random.shuffle(questions)

    for q in questions:
        correct_answer = q["answer"]
        options = q["options"]
        random.shuffle(options)

        q["answer"] = correct_answer
        q["options"] = options

    return questions

def ask_questions(questions):
    score = 0
    for i, q in enumerate(questions, 1):
        print(f"\nQ{i}: {q['question']}")
        for j, option in enumerate(q['options'], 1):
            print(f"  {j}. {option}")
        answer = input("Your answer (1-4): ").strip()
        if q['options'][int(answer)-1] == q['answer']:
            print("✅ Correct!")
            score += 1
        else:
            print(f"❌ Wrong! Correct answer: {q['answer']}")
    return score

def save_result(username, topic, score, total):
    from datetime import datetime

    result = {
        "username": username,
        "topic": topic,
        "score": f"{score}/{total}"
    }

    results_dir = os.path.join(os.path.dirname(__file__), "../../", "results")
    results_dir = os.path.abspath(results_dir)
    os.makedirs(results_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"result_{username}_{timestamp}.json"
    results_path = os.path.join(results_dir, filename)

    with open(results_path, 'w') as file:
        json.dump(result, file, indent=4)

    print(f"\n📁 Result saved to: {results_path}")

def main():
    print("🎓 Welcome to the Quiz App 🎓")
    username = get_username()
    topic = choose_topic()
    questions = load_questions(topic)
    score = ask_questions(questions)

    print(f"\n🏁 {username}, your final score for your chosen topic '{topic}' is: {score}/{len(questions)}")
    save_result(username, topic, score, len(questions))

if __name__ == "__main__":
    main()
