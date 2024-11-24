from pydantic.v1 import BaseModel

class ErrorResponse(BaseModel):
    error: str
