import os
import sys
from sqlalchemy.orm import Session

# Añadimos el directorio raíz del proyecto al path de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.shared.infra.db import SessionLocal, engine, Base
from src.shared.infra.seed import seed_initial_rooms

# Creamos las tablas
Base.metadata.create_all(bind=engine)

# Creamos una sesión
session = SessionLocal()

# Ejecutamos el seed
seed_initial_rooms(session)

print("Seed completado con éxito!")