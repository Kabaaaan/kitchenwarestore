from fastapi import APIRouter, HTTPException, Response, Depends, Cookie, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse

from api.v1.schemas.schemas import *
from api.api_config import *
from utils.auth import *
from database.models.models import User


router = APIRouter()
security = HTTPBearer()
users_orm = User()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    access_token = credentials.credentials
    access_token_data = get_token_payload(access_token)

    if access_token_data.get('message'):
        if access_token_data['message'] == "Invalid token":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")
        if access_token_data['message'] == "Token has expired":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token has expired")
    return access_token_data


@router.post("/login/token", summary='Получение пары jwt токенов.')
async def token(
    credentials: Credentials, 
    response: Response) -> JSONResponse:

    user_name = credentials.name
    user_password = credentials.password

    get_users = users_orm.select_all()

    if len(get_users) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found.")

    user_found = False
    for user in get_users:
        if user['name'] == user_name:
            user_found = True
            if user['password'] == user_password:
                payload = {
                    'id': user['id'],
                    'name': user_name,
                    'role': user['role']
                }

                access_token = create_token(token_type='access', payload=payload)
                refresh_token = create_token(token_type='refresh', payload=payload)

                content = {"Authorization": f"Bearer {access_token}",
                            "Refresh-Token": f"Bearer {refresh_token}"}

                response = JSONResponse(content=content, status_code=status.HTTP_200_OK)
                return response
            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong password.")

    if not user_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user found.")
    

@router.post("/login/create", summary='Создание пользователя')
async def create_user(
        credentials: Credentials, 
        response: Response) -> JSONResponse:
    
    user_name = credentials.name
    user_password = credentials.password

    operstion_result = users_orm.add_user(name=user_name, password=user_password, role='regular')

    if operstion_result['success'] == True:
        return JSONResponse(content=operstion_result, status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content=operstion_result, status_code=status.HTTP_409_CONFLICT)
    

@router.post("/login/refresh", summary='Рефреш токена.')
async def refresh_token(
    response: Response, 
    refresh_token: str = Header(None, alias="RefreshToken")) -> JSONResponse:

    if not refresh_token or not refresh_token.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token is missing or wrong format")

    refresh_token = refresh_token.split(" ")[1]
    refresh_token_data = get_token_payload(refresh_token)

    if refresh_token_data.get('message'):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token is invalid or expired")
    
    payload = {'id': refresh_token_data['id'],
               'name': refresh_token_data['name'],
               'role': refresh_token_data['role']}
    
    access_token = create_token(token_type='access', payload=payload)
    response = JSONResponse(content={"Authorization": f"Bearer {access_token}"}, status_code=status.HTTP_200_OK)
    
    return response


@router.get("/", summary='Получение списка пользователей. Param: limit - кол-во пользователей.')
async def get_users(
    response: Response, 
    current_user: dict = Depends(get_current_user)) -> JSONResponse:

    if not await check_role(user_role=current_user['role'], allowed_roles=['admin']):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=ACCESS_DENIED_MESSAGE)
    
    users = users_orm.select_all()
    if len(users) != 0:
        response_data = {'users': users}
        return JSONResponse(content=response_data, status_code=status.HTTP_200_OK)
    else: 
        return JSONResponse(content='No users found.', status_code=status.HTTP_404_NOT_FOUND)


@router.get("/me", summary='Получение информации об аккаунте авторизованного пользователя.')
async def get_user(
    response: Response, 
    current_user: dict = Depends(get_current_user)) -> JSONResponse:
    
    return JSONResponse(status_code=status.HTTP_200_OK, content=current_user)


@router.get("/{user_id}", summary='Получение пользователя по id.')
async def get_user_by_id(
    response: Response, 
    user_id: int, 
    current_user: dict = Depends(get_current_user)) -> JSONResponse:

    if not await check_role(user_role=current_user['role'], allowed_roles=['admin']):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=ACCESS_DENIED_MESSAGE)

    user = users_orm.select_item_by_id(item_id=user_id)
    if user != {'message': 'Not found.'}:
        return JSONResponse(content=user, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user found with the given ID.")


@router.delete("/{user_id}", summary='Удаление аккаунта пользователя.')
async def delete_user(
    response: Response, 
    user_id: int, 
    current_user: dict = Depends(get_current_user)) -> JSONResponse:

    if not await check_role(user_role=current_user['role'], allowed_roles=['admin']):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=ACCESS_DENIED_MESSAGE)
    
    users_orm.remove_item_by_id(item_id=user_id)
    return JSONResponse(content=f'User (id = {user_id}) successfully deleted.', status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{user_id}", summary='Обновление аккаунта пользователя.')
async def update_user(
    response: Response, 
    user_id: int, 
    user_data: UsersDataToUpdate, 
    current_user: dict = Depends(get_current_user)) -> JSONResponse:
    
    if not await check_role(user_role=current_user['role'], allowed_roles=['admin', 'regular']):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=ACCESS_DENIED_MESSAGE)
    
    message = users_orm.update_user_account(user_id=user_id,
                                            name=user_data.name,
                                            password=user_data.password,
                                            role=user_data.role)
    
    if message['success'] == True:
        return JSONResponse(content=message, status_code=status.HTTP_204_NO_CONTENT)
    else:
        return JSONResponse(content=message, status_code=status.HTTP_409_CONFLICT)
