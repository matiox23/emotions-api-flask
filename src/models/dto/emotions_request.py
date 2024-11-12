# src/models/dto/emotion_request_dto.py

from pydantic.v1 import BaseModel, validator
import base64

class EmotionRequestDto(BaseModel):
    id_usuario: int  # Añadido id_usuario
    img_base64: str

    @validator('img_base64')
    def validate_base64_image(cls, v):
        try:
            # Decodificar la parte base64 para validar
            if v.startswith("data:image"):
                v = v.split(",")[1]
            base64.b64decode(v)
        except Exception:
            raise ValueError("La imagen proporcionada no es una cadena base64 válida")
        return v
