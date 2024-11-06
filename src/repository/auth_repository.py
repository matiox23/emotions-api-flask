from sqlmodel import Session, select
from src.db.database import engine
from src.models.entity.user import User

class AuthRepository:
    @staticmethod
    def login(correo: str, password: str, tipo_usuario: str) -> User | None:
        with Session(engine) as session:
            user = session.exec(
                select(User).where(
                    User.correo == correo,
                    User.password == password,
                    User.tipo_usuario == tipo_usuario
                )
            ).first()
        return user
