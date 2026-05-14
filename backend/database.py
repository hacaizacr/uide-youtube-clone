import os
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv

# 1. Cargar las variables del archivo .env
load_dotenv()

# 2. Obtener la URL de conexión
DATABASE_URL = os.getenv("DATABASE_URL")

# 3. Configurar el motor de la base de datos
engine = create_engine(DATABASE_URL)

def init_db():
    """Crea las tablas en la RDS si no existen"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Provee una sesión de base de datos para los endpoints"""
    with Session(engine) as session:
        yield session