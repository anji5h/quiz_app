from datetime import datetime
from pydantic import BaseModel, RootModel
from typing import List, Dict, Union


# schema for config.json
class QuizConfig(BaseModel):
    appPassword: str
    topics: List[str]
    questionsPerTopic: int


# schema for data json file
class Question(BaseModel):
    question: str
    options: Dict[str, str]
    answer: str


class Quiz(RootModel[Dict[str, Question]]):
    pass


# schema for result.json
class Score(BaseModel):
    timestamp: str
    score: int
    total: int


class User(RootModel[Dict[str, List[Score]]]):
    pass


class Result(RootModel[Dict[str, User]]):
    pass
