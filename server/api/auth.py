from datetime import datetime, timedelta

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi import Depends, HTTPException, status, Request, Response

from server.model.auth import authenticate_user, Token, User, UserInDB, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_active_user, blacklist

BASE_URL = '/api/v1'

restapi = APIRouter(
    prefix=f"{BASE_URL}/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

@restapi.post("/token", response_model=Token)
async def login_for_access_token(request: Request):
    form_data = await request.json()
    user = authenticate_user( form_data['username'], form_data['password'] )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    response = Response(content='Success', status_code=200)
    response.set_cookie(key='access_token', value=access_token, httponly=True)
    return response


@restapi.get("/refresh", response_model=User)
async def read_users_me(request: Request, current_user: User = Depends(get_current_active_user)):
    token = request.cookies.get('access_token')    
    blacklist.add(token)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.username}, expires_delta=access_token_expires
    )

    response = Response(content='Success', status_code=200)
    response.set_cookie(key='access_token', value=access_token, httponly=True)
    return response


@restapi.get("/me", response_model=User)
async def read_users_me(request: Request, current_user: User = Depends(get_current_active_user)):
    return current_user


@restapi.delete("/token")
async def logout_user(request: Request, current_user: User = Depends(get_current_active_user)):
    token = request.cookies.get('access_token')    
    blacklist.add(token)

    response = Response(content='Success', status_code=200)
    response.set_cookie(key='access_token', value='deleted;', httponly=True)
    return response


