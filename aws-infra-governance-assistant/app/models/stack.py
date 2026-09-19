from datetime import datetime
from typing import List

from pydantic import BaseModel


class Stack(BaseModel):
    """Represents a CloudFormation stack and its status.

    Attributes:
        stack_name: The name of the CloudFormation stack.
        status: The current status of the stack.
        creation_time: The time the stack was created.
    """

    stack_name: str
    status: str
    creation_time: datetime


class StackListResponse(BaseModel):
    """Response containing a list of CloudFormation stacks.

    Attributes:
        count: The number of stacks returned.
        stacks: A list of stack records.
    """

    count: int
    stacks: List[Stack]