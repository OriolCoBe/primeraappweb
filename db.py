from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///database/proyecto_final.db',
                       connect_args={'check_same_thread': False})  # Lenguaje y dirección de la db

Session = sessionmaker(bind=engine)  # La session nos permite hacer operaciones en nuestra db
session = Session()
Base = declarative_base()
