from pathlib import Path
from sqlmodel import SQLModel, create_engine, Session, select, func
from models import Ville


# Crée le dossier db/ si il n'existe pas
Path("db").mkdir(exist_ok=True)

# Charge le moteur de bdd, la crée avant si elle n'existe pas
engine = create_engine("sqlite:///db/meteo.db")


NOM_VILLE_SQ = "Saint-Quentin"
PARAMETRES_SQ = {
    "latitude": 49.8489,
    "longitude": 3.2876,
}


def init_db():
    SQLModel.metadata.create_all(engine)

    # Initialise toujours la ligne Saint-Quentin si elle n'existe pas dans la bdd
    with get_session() as session:
        saint_quentin = session.exec(select(Ville).where(Ville.nom == NOM_VILLE_SQ)).first()
        if not saint_quentin:
            session.add(Ville(nom=NOM_VILLE_SQ, latitude=PARAMETRES_SQ["latitude"], longitude=PARAMETRES_SQ["longitude"]))
            session.commit()


# Fonction de session bdd
def get_session() -> Session:
    return Session(engine)
