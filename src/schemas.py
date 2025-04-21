from pydantic import BaseModel, RootModel, field_validator
from typing import List, Dict


# schema for admin.json
class QuizConfig(BaseModel):
    appPassword: str
    categories: List[str]
    questionsPerTopic: int


# schema for quiz.json
class Question(BaseModel):
    question: str
    a: str
    b: str
    c: str
    d: str
    answer: str


class Topic(RootModel[Dict[str, Question]]):
    pass


class Quiz(RootModel[Dict[str, Topic]]):
    pass
