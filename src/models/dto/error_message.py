from pydantic.v1 import BaseModel

class ErrorResponseMessage(BaseModel):
    error: str