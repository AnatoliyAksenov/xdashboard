from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from passlib.context import CryptContext
from pydantic import BaseModel
import ldap3
from ldap3 import Server, Connection, ALL

import server.sources.corp as corp


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d66e094faa6ca2556c81996600a9563b93f7099f6f0f4caa6cf66688e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    cn: Optional[str] = None
    sn: Optional[str] = None


class UserInDB(User):
    id: int
    acl: Optional[list] = list()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

ldap_server = Server('localhost', get_info=ALL)

# TODO: Move blacklist to redis
blacklist = set()

def verify_password(username, password):

    #return pwd_context.verify(plain_password, hashed_password)
    lstring = f'sAMAccountName={username},ou=people,dc=example,dc=org'
    conn = Connection(ldap_server, user=lstring, password=password, auto_bind=True, raise_exceptions=True)

    return conn.result['description'] == 'success'


def get_user(username: str):
    q = """SELECT t.*,
                  sAMAccountName username, 
                  isd            disabled,
                  mail           email                  
            FROM auth.tbl_users t 
           WHERE sAMAccountName = %(username)s"""

    res = corp.get_data(q, {"username": username})
    if res:
        user_dict = res[0]
        # read user permissions
        qq = """
            SELECT r.key role_key
            FROM auth.tbl_user_to_role rtl
            JOIN auth.tbl_roles r on r.key = rtl.role_key
            WHERE rtl.user_id = %(id)s
            """
        res = corp.get_data(qq, {"id": user_dict['id']}) 
        user_dict['acl'] = [x['role_key'] for x in res]
        return UserInDB(**user_dict)

    return None


def authenticate_user(username: str, password: str):

    user = get_user(username)

    if not user:
        return False

    if not verify_password(user.username, password):
        return False

    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(request: Request):
    token = request.cookies.get('access_token')

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Сheck token in blacklist
    # TODO: Move blacklist to redis
    if token in blacklist:
        raise credentials_exception
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData( username=username )
    except JWTError:
        raise credentials_exception
    
    user = get_user( username=token_data.username )
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """Check authentication without checking any user permissions
    """    
    return current_user


def check_user_permissions(required_acls):
    """Check user permissions
    """
    async def result_func(current_user: User = Depends(get_current_user)):
        if current_user.acl:
            if len(set(required_acls) - set(current_user.acl)) > 0:
                raise HTTPException(status_code=403, detail="Permission denied")
        return current_user
    return result_func