# Quiz Management System

The Quiz Management System is a Python-based application that allows administrators to manage quiz questions and users to take quizzes on various topics. It consists of two main scripts:
- **Admin Code (`admin.py`)**: For administrators to add or delete quiz questions.
- **Client Code (`client.py`)**: For users to take quizzes and view their scores.

The system uses JSON files for configuration, question storage, and result tracking, with data validation via Pydantic schemas.

## Features
- **Admin Features**:
  - Add questions to topics with four options and a correct answer.
  - Delete questions by ID.
  - Password-protected admin access.
- **Client Features**:
  - Select a username and topic to take a quiz.
  - Answer randomized questions with immediate feedback.
  - Save and track quiz results with timestamps.
- **Data Management**:
  - Stores configuration, questions, and results in JSON files.
  - Validates data using schemas for consistency.

## Prerequisites
- Python 3.8+
- Required packages: `pydantic` (for schema validation)
  ```bash
  pip install -r requirements.txt
  ```

## Project Structure
```
quiz-system/
├── config/
│   └── config.json        # Configuration file (topics, admin password, etc.)
├── data/
│   └── <topic>.json       # Question files for each topic (e.g., python_quiz.json)
├── result/
│   └── result.json        # User quiz results
├── schemas.py             # Pydantic schema definitions
├── admin.py               # Admin script for managing questions
├── client.py              # Client script for taking quizzes
└── README.md              # Project documentation
|__ requirements.txt       # Project Dependency
```

## Setup
1. **Clone or Create the Project Directory**:
   Create a directory for the project and place `admin.py`, `client.py`, and `schemas.py` in it.

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create `schemas.py`**:
   Create a `schemas.py` file with the following Pydantic models:
   ```python
   from pydantic import BaseModel
   from typing import Dict, List

   class Question(BaseModel):
       question: str
       options: Dict[str, str]
       answer: str

   class Quiz(BaseModel):
       root: Dict[str, Question]

   class QuizConfig(BaseModel):
       appPassword: str
       topics: List[str]
       questionsPerTopic: int

   class Score(BaseModel):
       timestamp: str
       score: int
       total: int

   class User(BaseModel):
       root: Dict[str, List[Score]]

   class Result(BaseModel):
       root: Dict[str, User]
   ```

4. **Create `config.json`**:
   In the `config` directory, create `config.json` with the following structure:
   ```json
   {
       "appPassword": "admin123",
       "topics": ["python_quiz", "general_knowledge"],
       "questionsPerTopic": 10
   }
   ```

5. **Initialize Directories**:
   Create empty `data` and `result` directories. The scripts will automatically create JSON files as needed.

## Usage
### Admin Mode (`admin.py`)
1. Run the admin script:
   ```bash
   python admin.py
   ```
2. Enter the admin password (e.g., `admin123`).
3. Choose an option:
   - **1. Add question to topic**: Select a topic, enter question text, four options, and the correct answer.
   - **2. Delete question from topic**: Select a topic and enter the question ID to delete.
   - **3. Exit**: Close the program.
4. Questions are saved in `data/<topic>.json`.

### Client Mode (`client.py`)
1. Run the client script:
   ```bash
   python client.py
   ```
2. Enter your username.
3. Choose a topic from the displayed list.
4. Answer each question by entering a number (1–4).
5. View your score and feedback after completing the quiz.
6. Results are saved in `result/result.json`.

## Example Files
- **Question File (`data/python_quiz.json`)**:
  ```json
  {
      "uuid1": {
          "question": "What is 2 + 2?",
          "options": {
              "1": "3",
              "2": "4",
              "3": "5",
              "4": "6"
          },
          "answer": "2"
      }
  }
  ```
- **Result File (`result/result.json`)**:
  ```json
  {
      "Alice": {
          "python_quiz": [
              {
                  "timestamp": "2025-05-01 10:00:00",
                  "score": 2,
                  "total": 2
              }
          ]
      }
  }
  ```

## Notes
- Ensure `config.json` lists valid topics, and create corresponding `<topic>.json` files in the `data` directory using the admin script.
- The admin password is stored in plain text; consider hashing for production use.
- Quiz results are appended to `result.json` and may grow large over time.
