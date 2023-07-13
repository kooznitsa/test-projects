from datetime import datetime, timedelta
from secrets import token_bytes
from base64 import b64encode

from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlmodel import select

from db.errors import UserCredentialsError
from repositories.base import BaseRepository
from schemas.tokens import TokenData
from schemas.users import User, UserRead


SECRET_KEY = b64encode(token_bytes(32)).decode()
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class UserRepository(BaseRepository):
    model = User

    async def _get_user(self, username: str) -> UserRead:
        user = await self.session.exec(select(self.model).where(User.username == username))
        if user := user.first():
            return UserRead.from_orm(user)
        else:
            raise UserCredentialsError

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def get(self, token: str) -> UserRead:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get('sub')
            if username is None:
                raise UserCredentialsError
            token_data = TokenData(username=username)
        except JWTError:
            raise UserCredentialsError
        user = await self._get_user(token_data.username)
        if user is None:
            raise UserCredentialsError
        return user

    async def login(self, form_data: OAuth2PasswordRequestForm):
        query = select(self.model).where(self.model.username == form_data.username)
        user = await self.session.exec(query)
        user = user.first()
        if user and user.verify_password(form_data.password):
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = self.create_access_token(
                data={'sub': user.username}, expires_delta=access_token_expires
            )
            return {'access_token': access_token, 'token_type': 'bearer'}
        else:
            raise UserCredentialsError