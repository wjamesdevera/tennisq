from pydantic import BaseModel
from enum import Enum
from typing import Optional


class ResponseStatus(Enum):
    SUCCESS: str = 'success'
    FAIL: str = 'fail'
    ERROR: str = 'error'


class ResponseFormat(BaseModel):
    status: ResponseStatus
    data: Optional[any]
    message: Optional[any]
    code: Optional[int]
