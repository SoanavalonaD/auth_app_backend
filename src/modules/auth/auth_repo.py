from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.modules.auth.auth_model import User
from src.modules.auth.auth_dto import UserCreate

class UserRepository:
    """
    Interface entre les services métier et la base de données.
    Contient la logique d'accès aux données (CRUD).
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def create_user(self, user_in: UserCreate, hashed_password: str) -> User:
        db_user = User(
            email=user_in.email,
            hashed_password=hashed_password,
            is_active=True
        )
        self.db.add(db_user)
        # Commit implicite géré par la dépendance get_db_session
        await self.db.flush() # Force l'ID à être rempli sans commit
        return db_user