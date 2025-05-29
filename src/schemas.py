from pydantic import BaseModel, RootModel, field_validator, Field
from typing import List, Dict
from datetime import datetime
import re

# Schema for config.json
class QuizConfig(BaseModel):
    topics: List[str]
    questionsPerTopic: int

# Schema for quiz_<topic>.json
class Question(BaseModel):
    question: str
    options: Dict[str, str]
    answer: str
class Quiz(RootModel[Dict[str, Question]]):
    pass

# Schema for scores.json
class Score(BaseModel):
    timestamp: str
    score: int
    total: int

class User(RootModel[Dict[str, List[Score]]]):
    pass

class Result(RootModel[Dict[str, User]]):
    pass

# Schema for users.json
class UserCredentials(BaseModel):
    username: str
    password: str
    role: str

    @field_validator("username")
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError("Username must contain only letters, numbers, underscores, or hyphens")
        return v

    @field_validator("role")
    def validate_role(cls, v):
        if v not in {"USER", "ADMIN"}:
            raise ValueError("Role must be 'USER' or 'ADMIN'")
        return v

class Users(RootModel[Dict[str, UserCredentials]]):
    pass