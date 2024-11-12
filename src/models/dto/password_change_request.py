from pydantic.v1 import BaseModel

class PasswordChangeRequest(BaseModel):
    correo: str
    old_password: str
    new_password: str