from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.data.domain import get_db_session
from src.modules.auth.auth_dto import UserCreate, UserInDB, Token
from src.modules.auth.auth_repo import UserRepository
from src.modules.auth.auth_app import get_password_hash, verify_password, create_access_token
from src.modules.auth.auth_model import User

class AuthAppService:
    """
    Orchestre le Repository et la Logique Métier.
    Contient la logique de haut niveau de l'application (inscription, connexion).
    """
    def __init__(self, db: AsyncSession = Depends(get_db_session)):
        self.repository = UserRepository(db)

    async def register_new_user(self, user_in: UserCreate) -> UserInDB:
        """Logique d'inscription: vérifie l'existence, hache le mot de passe et crée l'utilisateur."""
        
        # 1. Vérification de l'existence (Logique Métier/Repository)
        existing_user = await self.repository.get_user_by_email(user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Un utilisateur avec cet email existe déjà"
            )

        # 2. Hachage du mot de passe (Service Métier)
        hashed_password = get_password_hash(user_in.password)
        
        # 3. Création de l'utilisateur (Repository)
        db_user = await self.repository.create_user(user_in, hashed_password)
        
        # 4. Retour du schéma de sortie
        return UserInDB.model_validate(db_user)

    async def authenticate_user(self, user_login: UserCreate) -> Token:
        """Logique de connexion: vérifie les identifiants et génère un token JWT."""
        
        # 1. Récupération de l'utilisateur (Repository)
        user: User | None = await self.repository.get_user_by_email(user_login.email)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou mot de passe incorrect"
            )
            
        # 2. Vérification du mot de passe (Service Métier)
        if not verify_password(user_login.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou mot de passe incorrect"
            )
            
        # 3. Vérification de l'état (Logique Métier)
        if not user.is_active:
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Compte inactif"
            )

        # 4. Création du Token JWT (Service Métier)
        access_token = create_access_token(data={"sub": str(user.id)})
        
        # 5. Retour du schéma de sortie
        return Token(access_token=access_token)