from sqlalchemy.future import select

from app.models.user import User
from app.schemas.user import UserCreate
from app.services.base import BaseService
from app.core.security import get_password_hash, verify_password


class UserService(BaseService):
    async def authenticate(self, email: str, password: str) -> User | None:
        user = await self.db.execute(select(User).where(User.email == email))
        user = user.scalar_one_or_none()
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(self, user_in: UserCreate) -> User:
        user = User(
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password),
            is_active=True,
        )
        self.db.add(user)
        await self.commit()
        await self.refresh(user)
        return user
