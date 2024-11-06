from sqlmodel import select, Session
from src.db.database import engine
from src.models.entity.emotions import Emotions

class EmotionRepository:

    @staticmethod
    def get_all():
        with Session(engine) as session:
            emotions = session.exec(select(Emotions)).all()
        return emotions


    @staticmethod
    def add(emotion: Emotions):
        with Session(engine) as session:
            session.add(emotion)
            session.commit()
            session.refresh(emotion)
        return emotion
