from pydantic.v1 import BaseModel

class MessageResponse(BaseModel):
    message: str