from pydantic import BaseModel, RootModel, field_validator, Field
from typing import List, Dict
from datetime import datetime
import re

# Schema for config.json
class QuizConfig(BaseModel):
    topics: List[str]
    questionsPerTopic: int = Field(..., gt=0)  # Must be positive

    @field_validator("topics")
    def validate_topics(cls, v):
        for topic in v:
            if not re.match(r'^[a-zA-Z0-9_-]+$', topic):
                raise ValueError(f"Invalid topic name: {topic}")
        return v

# Schema for quiz_<topic>.json
class Question(BaseModel):
    question: str
    options: Dict[str, str]
    answer: str

    @field_validator("options")
    def validate_options(cls, v):
        if len(v) != 4:
            raise ValueError("Must have exactly 4 options")
        if set(v.keys()) != {"1", "2", "3", "4"}:
            raise ValueError("Option keys must be '1', '2', '3', '4'")
        return v

    @field_validator("answer")
    def validate_answer(cls, v, values):
        if "options" in values and v not in values["options"]:
            raise ValueError("Answer must be a valid option key")
        return v

class Quiz(RootModel[Dict[str, Question]]):
    pass

# Schema for scores.json
class Score(BaseModel):
    timestamp: datetime
    score: int
    total: int

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}

class User(RootModel[Dict[str, List[Score]]]):
    pass

class Result(RootModel[Dict[str, User]]):
    pass

# Schema for users.json
class UserCredentials(BaseModel):
    username: str
    password: str  # Hashed password
    role: str  # "USER" or "ADMIN"

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