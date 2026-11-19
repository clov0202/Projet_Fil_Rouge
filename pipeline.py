import requests
from pydantic import ValidationError
from sqlmodel import select, func
from database import init_db, get_session
from models import Ville, Releve, WeatherResponseModel


URL = "https://api.open-meteo.com/v1/forecast"


def collecter(nom: str) -> Releve | None:
    """
    Lit les coordonnées de la ville et enregistre le relevé récupéré.
    """
    init_db() # Initialise la base si besoin
    
    try:
        with get_session() as session:
            # 1. Recherche de la ville en base (insensible à la casse)
            ville = session.exec(select(Ville).where(func.lower(Ville.nom) == nom.lower())).first()
            if not ville:
                raise ValueError(f"La ville '{nom}' n'existe pas en base de données.")

            parametres = {
                "latitude": ville.latitude,
                "longitude": ville.longitude,
                "current_weather": True         # CURRENT_WEATHER = True
            }

            # Appel HTTP et validation Pydantic
            res = requests.get(URL, params=parametres, timeout=5)
            res.raise_for_status()
            
            donnees = WeatherResponseModel(**res.json())
            meteo = donnees.current_weather

            # Enregistrement du relevé
            releve = Releve(
                temperature=meteo.temperature,
                vitesse_vent=meteo.windspeed,
                date_heure=meteo.time,
                ville=ville
            )
            session.add(releve)
            session.commit()
            session.refresh(releve)

            # Affichage du relevé valide dans le terminal
            print(f"[OK] {ville.nom} : {meteo.temperature}°C, vent {meteo.windspeed} km/h ({meteo.time})")
            return releve

    except ValueError as e:
        print(f"[Erreur Base] : {e}")
        raise
    except requests.RequestException as e:
        print(f"[Erreur Réseau] : {e}")
        raise
    except ValidationError as e:
        print(f"[Erreur Validation] : {e}")
        raise


if __name__ == "__main__":
    collecter('Saint-Quentin')
