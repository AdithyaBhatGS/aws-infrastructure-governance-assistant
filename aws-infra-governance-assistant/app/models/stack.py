from datetime import datetime
from typing import List

from pydantic import BaseModel

class Stack(BaseModel):
    stack_name: str

    status: str

    creation_time: datetime

class StackListResponse(BaseModel):
    count: int

    stacks: List[Stack]