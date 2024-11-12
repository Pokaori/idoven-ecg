from argparse import ArgumentParser
import asyncio
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.services.user import UserService
from app.schemas.user import UserCreate


async def create_admin_user(email: str, password: str, session: AsyncSession) -> None:
    """Create an admin user with the given email and password."""
    # Check if user already exists
    user_service = UserService(session)
    user = await user_service.get_by_email(email)
    if user:
        print(f"User with email {email} already exists")
        return

    user = await user_service.create_admin(UserCreate(email=email, password=password))

    print(f"Admin user {email} created successfully")


async def main(email: str, password: str) -> None:
    """Main function to create admin user."""
    async with AsyncSessionLocal() as session:
        await create_admin_user(email, password, session)


if __name__ == "__main__":
    parser = ArgumentParser(description="Create an admin user")
    parser.add_argument("--email", required=True, help="Admin user email")
    parser.add_argument("--password", required=True, help="Admin user password")

    args = parser.parse_args()

    asyncio.run(main(args.email, args.password))
