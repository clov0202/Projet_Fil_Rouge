from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship


# Validation de la réponse Open-Meteo (Partie 1)
class CurrentWeatherSchema(BaseModel):
    temperature: float
    windspeed: float
    time: str


class WeatherResponseModel(BaseModel):
    latitude: float
    longitude: float
    current_weather: CurrentWeatherSchema


# Tables SQLite + Schémas Swagger (Parties 2 & 3)
class Ville(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nom: str = Field(unique=True)
    latitude: float
    longitude: float
    releves: list["Releve"] = Relationship(back_populates="ville")


class Releve(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    ville_id: int = Field(foreign_key="ville.id")
    temperature: float
    vitesse_vent: float
    date_heure: str
    ville: Ville | None = Relationship(back_populates="releves")
