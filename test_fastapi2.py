from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
auth_schem = OAuth2PasswordBearer(tokenUrl="token")


class UserInDB(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str


class UserOut(BaseModel):
    username: str
    email: str


class TokenData(BaseModel):
    access_token: str
    token_type: str


app = FastAPI()

pw = CryptContext(schemes=['bcrypt'])
users_db = {'shajahan': {'username': 'shajahan',
                         'hashed_password': '$2b$12$toFL82l0NsWMZX6kEzeWhOiFOZI3HqTnQVQ3EpgBusCd9LzrfDrZK',
                         'email': 'shajahan@nttdata.com'
                         }}


def hash_password(password):
    return pw.hash(password)


def get_user(users_db, username):
    if username in users_db:
        return UserInDB(**users_db[username])


def verify_password(password, hashed_password):
    return pw.verify(password, hashed_password)


def authenticate(data):
    user = get_user(users_db, data.username)
    if user is None:
        raise HTTPException(
            status_code=404, detail="User not found, please register")
    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Unauthorized user"
        )
    # return UserOut(**user.model_dump())
    return user


def create_token(username, expire_time_in_mins):
    to_encode = {'sub': username, 'exp': datetime.now(
        timezone.utc)+timedelta(minutes=expire_time_in_mins)}
    token = jwt.encode(to_encode, 'super_secret', algorithm='HS256')
    return TokenData(**{'access_token': token, 'token_type': 'bearer'})


@app.post("/token", response_model=TokenData)
def get_token(data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    print(data.username, data.password)
    user = authenticate(data)
    token = create_token(user.username, expire_time_in_mins=30)
    return token


@app.post("/register", response_model=UserOut)
def register_user(data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    users_db[data.username] = {
        'username': data.username, 'hashed_password': pw.hash(data.password), 'email': data.username+"@nttdata.com"}
    return users_db[data.username]


def get_current_user(token: Annotated[str, Depends(auth_schem)]):
    try:
        payload = jwt.decode(token, 'super_secret', algorithms=['HS256'])
        print(payload)
        user = get_user(users_db, payload['sub'])
        if user is None:
            raise HTTPException(status_code=404, detail='user not found')
        return user
    except InvalidTokenError:
        raise HTTPException(status_code=400, detail='invalid token')


@app.get("/getu/ser/me", response_model=UserOut)
def get_username(user: Annotated[UserInDB, Depends(get_current_user)]):
    print(user.model_dump())
    return user
