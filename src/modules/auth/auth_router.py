from fastapi import APIRouter, Depends, status
from src.modules.auth.auth_dto import UserCreate, UserInDB, Token, UserLogin
from src.modules.auth.auth_app import AuthAppService

router = APIRouter(
    prefix="/auth",
    tags=["Authentification"],
)

@router.post(
    "/register", 
    response_model=UserInDB, 
    status_code=status.HTTP_201_CREATED,
    summary="Enregistrer un nouvel utilisateur",
)
async def register(
    user_in: UserCreate, 
    auth_service: AuthAppService = Depends()
):
    """
    Point de terminaison pour l'inscription d'un nouvel utilisateur.
    Appelle le Service Applicatif pour gérer la logique d'inscription.
    """
    return await auth_service.register_new_user(user_in)

@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Authentification de l'utilisateur et obtention d'un jeton JWT",
)
async def login(
    user_login: UserLogin,
    auth_service: AuthAppService = Depends()
):
    """
    Point de terminaison pour la connexion.
    Valide les identifiants et retourne un jeton d'accès JWT.
    """
    return await auth_service.authenticate_user(user_login)