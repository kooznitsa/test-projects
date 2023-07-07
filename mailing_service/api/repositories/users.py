from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

from db.errors import UserCredentialsError
from repositories.base import BaseRepository
from schemas.users import User, UserRead


class UserRepository(BaseRepository):
    model = User

    async def get(self, token: str) -> UserRead:
        user = await self.session.exec(select(User).where(User.username == token))
        if user := user.first():
            return UserRead.from_orm(user)
        else:
            raise UserCredentialsError

    async def login(self, form_data: OAuth2PasswordRequestForm):
        query = select(User).where(User.username == form_data.username)
        user = await self.session.exec(query)
        user = user.first()
        if user and user.verify_password(form_data.password):
            return {'access_token': user.username, 'token_type': 'bearer'}
        else:
            raise UserCredentialsError
