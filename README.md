# 📚 Quiz Application (Beta)

## Description

The **Quiz Application (Beta)** is a desktop-based educational tool designed to help students and educators manage quizzes and track performance. Users can:

- Log in and take quizzes
- View personalized score analytics over time
- Admins can add or delete questions

This beta version serves as the foundation for future features like user registration, enhanced analytics, and improved UI functionality.

---

## ⚙️ Installation and Setup

### Prerequisites

- **Python Version**: 3.11 or higher  
- **Operating System**: Windows, macOS, or Linux  
- **Required Libraries**:  
  Listed in `requirements.txt`

---

### Setup Instructions

#### Clone or Download the Project

```bash
# Option 1: Clone the repository
git clone https://github.com/yourusername/quiz_app_beta.git

# Option 2: Download the ZIP and extract it
unzip quiz_app_beta.zip
cd quiz_app_beta
```

#### Set Up a Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate the environment:

- **Windows**:
  ```bash
  venv\Scripts\activate
  ```
- **macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

#### Install Required Dependencies

```bash
pip install -r requirements.txt
```

Verify installation:

```bash
python -c "import matplotlib, seaborn, pydantic; print('All libraries installed')"
```

---

### Prepare the `data/` Directory

Ensure your project structure looks like this:

```
src
├── config
│   └── config.json
├── data
│   ├── art.json
│   ├── computer_science.json
│   ├── geography.json
│   ├── history.json
│   ├── literature.json
│   ├── mathematics.json
│   ├── movies.json
│   ├── science.json
│   └── sports.json
├── frames
│   ├── add_question_frame.py
│   ├── admin_frame.py
│   ├── analytics_frame.py
│   ├── auth_frame.py
│   ├── delete_question_frame.py
│   ├── leaderboard_frame.py
│   ├── manage_questions_frame.py
│   ├── quiz_frame.py
│   ├── user_analytics_frame.py
│   ├── user_frame.py
│   └── __init__.py
├── result
│   └── scores.json
├── users
│   └── users.json
├── data_manager.py
├── quiz_app.py
└── schemas.py
```

#### Example Data Files

**config/config.json**
```json
{
  "topics": ["art", "computer_science"],
  "questionsPerTopic": 10
}
```

**result/scores.json**
```json
{
  "anjish": {
    "art": [
      {
        "timestamp": "2025-05-29T15:53:55.175958",
        "score": 3,
        "total": 10
      }
    ],
    "computer_science": [
      {
        "timestamp": "2025-05-29T19:03:11.956226",
        "score": 5,
        "total": 10
      }
    ]
  }
}
```

**users/users.json**
```json
{
  "anjish": {
    "username": "anjish",
    "password": "password123",
    "role": "admin"
  }
}
```

**data/art.json**
```json
{
  "1": {
    "question": "What is the capital of France?",
    "options": {
      "1": "Paris",
      "2": "London",
      "3": "Berlin",
      "4": "Madrid"
    },
    "answer": "1"
  }
}
```

**data/computer_science.json**
```json
{
  "1": {
    "question": "What does CPU stand for?",
    "options": {
      "1": "Central Processing Unit",
      "2": "Control Processing Unit",
      "3": "Central Power Unit",
      "4": "Control Power Unit"
    },
    "answer": "1"
  }
}
```

---

## 🚀 Running the Application

Activate the virtual environment:

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

Navigate to the `src/` directory:

```bash
cd src
```

Run the application:

```bash
python quiz_app.py
```

**Default admin login:**

- **Username**: `admin`
- **Password**: `admin`

---

## 🧑‍💻 Usage Instructions

### Login Screen

- Enter username and password.
- Click **Login** or **Exit** to quit.

### Dashboard (After Login)

#### Admin Users

- **Manage Questions**: Add or delete questions by topic.
- **View Analytics**: View score progression charts.
- **Logout**: Return to login screen.

#### Regular Users

- **View Analytics**
- **Logout**

### Manage Questions

- **Add**: Select topic → input question, 4 options, and correct answer → Save.
- **Delete**: Select topic → choose question → Delete Selected.

### View Analytics

- Displays a line chart of user scores over time.
- X-axis: Timestamps  
- Y-axis: Score percentage (0–100%)

---

## ❗ Troubleshooting

| Issue | Solution |
|-------|----------|
| **App doesn't start** | Verify JSON files exist and are correctly formatted. |
| **Missing libraries** | Run `pip install -r requirements.txt` again. |
| **Analytics chart missing** | Check that `scores.json` has entries for the logged-in user. |

---

## 📦 Required Libraries

These are installed via `requirements.txt`:

- `matplotlib` – score progression charts  
- `seaborn` – enhanced chart styling  
- `pydantic` – schema validation  
- `tkinter` – GUI framework (included with Python)

---

## 🔮 Future Improvements

- User registration and authentication  
- Dynamic chart resizing and extra metrics  
- Enhanced error handling and backup features

---

## 🧪 Additional Tips

- Use virtual environments to isolate dependencies.
- You can expand `users/users.json` and `result/scores.json` to simulate more users or results.
- Update file paths in `DataManager` if relocating the `data/` folder.
