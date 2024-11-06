from deepface.models.demography import Emotion
from h5py.h5o import exists_by_name
from sqlmodel import Session,select
from src.db.database import engine
from src.models.entity import user
from src.models.entity.user import User


class UserRepository:
    @staticmethod
    def get_all():
        with Session(engine) as session:
            emotions = session.exec(select(User)).all()
        return emotions

    @staticmethod
    def add(user: User):
        with Session(engine) as session:
            session.add(user)
            session.commit()
            session.refresh(user)
        return user

    @staticmethod
    def update(user: User):
        with Session(engine) as session:
            session.add(user)
            session.commit()
            session.refresh(user)
        return user

    @staticmethod
    def delete(user_id:int) -> User | None:
        with Session(engine) as session:
            user = session.get(User, user_id)
            if user:
                session.delete(user)
                session.commit()
        return user


    @staticmethod
    def exists_by_correo(user_correo:str) -> bool:
        with Session(engine) as session:
            exists = session.exec(select(User).where(User.correo == user_correo)).first() is not None
        return  exists

    @staticmethod
    def get_by_id(user_id:int) -> User | None:
        with Session(engine) as session:
            user = session.get(User, user_id)
        return user



