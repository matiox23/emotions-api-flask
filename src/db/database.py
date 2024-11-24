from sqlmodel import SQLModel, create_engine
from src.models.entity.examen import Examen
from src.models.entity.pregunta import Pregunta
from src.models.entity.opcion_respuesta import OpcionRespuesta
from src.models.entity.resultado import Resultado
from src.models.entity.user import User
from src.models.entity.emotions import Emotions
from src.models.entity.profesor import Profesor
from src.models.entity.alumno import Alumno


postgres_user = "postgres.cgngeqagaxepijiclnwp"
postgres_password = "Navidada042302*"
postgres_host = "aws-0-sa-east-1.pooler.supabase.com"
postgres_port = "6543"
postgres_db = "face_net_supa"

postgres_url = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"

engine = create_engine(postgres_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)