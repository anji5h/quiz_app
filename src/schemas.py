from pydantic import BaseModel, RootModel
from typing import List, Dict


# schema for admin.json
class QuizConfig(BaseModel):
    appPassword: str
    topics: List[str]
    questionsPerTopic: int


# schema for quiz.json
class Question(BaseModel):
    question: str
    a: str
    b: str
    c: str
    d: str
    answer: str


class Quiz(RootModel[Dict[str, Question]]):
    pass
