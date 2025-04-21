from pydantic import BaseModel
from typing import List

class QuizConfig(BaseModel):
    appPassword: str
    categories: List[str]
    questionsPerTopic: int