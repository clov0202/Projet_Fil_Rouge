from requests import RequestException
from pydantic import ValidationError
from fastapi import FastAPI, HTTPException
from sqlmodel import select, func
from database import init_db, get_session
from models import Ville, Releve
from pipeline import collecter



# Crée l'application FastAPI
app = FastAPI(title="L'Observatoire Météo (Saint-Quentin)")


# Initialise la bdd au lancement
@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/", tags=["Accueil API"])
def accueil():
    """
    Page d'accueil 127.0.0.1
    """
    return {
        "message": "Bienvenue sur l'API de l'Observatoire Météo",
        "documentation": "http://127.0.0.1:8000/docs"
    }


# En GET pour les tests de collectes, on preferera POST pour les méthode qui modifient la bdd.
@app.get("/collecter/{nom}", response_model=Releve, status_code=201, tags=["Collecte Nouveau Relevé"])  #  http://localhost:8000/collecter/Saint-Quentin
def declencher_collecte(nom: str):
    """
        Collecte et enregistre un relevé pour une ville

        Ville disponible actuellement : `Saint-Quentin`
    """
    try:
        return collecter(nom)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except (RequestException, ValidationError) as e:
        raise HTTPException(status_code=502, detail=f"Erreur lors de la récupération météo : {e}")


@app.get("/meteo/{nom}", response_model=Releve, tags=["Lire Relevé Météo"])  #  http://localhost:8000/meteo/Saint-Quentin
def lire_dernier_releve(nom: str):
    """
        Retourne le dernier relevé enregistré pour une ville.
    """
    with get_session() as session:
        ville = session.exec(select(Ville).where(func.lower(Ville.nom) == nom.lower())).first()
        if not ville or not ville.releves:
            raise HTTPException(status_code=404, detail="Ville ou relevé introuvable")
        return ville.releves[-1]


@app.get("/historique/{nom}", response_model=list[Releve], tags=["Lire Historique Météo"])  #  http://localhost:8000/historique/Saint-Quentin
def lire_historique(nom: str):
    """
        Retourne tous les relevés enregistrés en base pour une ville.
    """
    with get_session() as session:
        ville = session.exec(select(Ville).where(func.lower(Ville.nom) == nom.lower())).first()
        if not ville:
            raise HTTPException(status_code=404, detail="Ville introuvable")
        return ville.releves


@app.get("/stats/{nom}", tags=["Statistiques Relevés"])  #  http://localhost:8000/stats/Saint-Quentin
def statistiques_ville(nom: str):
    """
        Calcule la moyenne, le min et le max des températures enregistrées.
    """
    with get_session() as session:
        ville = session.exec(select(Ville).where(func.lower(Ville.nom) == nom.lower())).first()
        if not ville or not ville.releves:
            raise HTTPException(status_code=404, detail="Aucune donnée disponible")
        
        temperatures = [r.temperature for r in ville.releves]
        return {
            "ville": ville.nom,
            "nombre_releves": len(temperatures),
            "temp_moyenne": round(sum(temperatures) / len(temperatures), 2),
            "temp_min": min(temperatures),
            "temp_max": max(temperatures)
        }
