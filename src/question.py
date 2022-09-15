from dataclasses import dataclass
from typing import List


@dataclass
class Question:
    wording: str
    possible_answers: List[str]
    correct_answer_indices: List[int]
