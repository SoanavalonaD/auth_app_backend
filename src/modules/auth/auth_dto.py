from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional

# Schémas de base/DTO pour l'Entrée (Création/Mise à jour)
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Schémas de Sortie (Réponse API)
class UserInDB(BaseModel):
    """Schéma Pydantic représentant les données de l'utilisateur dans la DB."""
    id: int
    email: EmailStr
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    """Schéma Pydantic pour la réponse JWT (Access Token)."""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Schéma Pydantic pour les données contenues dans le token (Payload)."""
    user_id: Optional[int] = None