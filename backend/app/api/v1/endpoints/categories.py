from fastapi import APIRouter, HTTPException, Response, Depends, status
from fastapi.responses import JSONResponse
from api.v1.endpoints.users import get_current_user

from api.v1.schemas.schemas import *
from api.api_config import *
from utils.auth import *
from database.models.models import Category


router = APIRouter()
category_orm = Category()

@router.get("/", summary='Получение списка категорий товаров.')
async def get_categories(response: Response) -> JSONResponse:
    categories = category_orm.select_all()

    if len(categories) != 0:
        response_data = {'Count': len(categories), 'categories': categories}
        return JSONResponse(content=response_data, status_code=status.HTTP_200_OK)
    else: 
        return JSONResponse(content='No categories found.', status_code=status.HTTP_404_NOT_FOUND)


@router.get("/{category_id}", summary='Получение категории товаров по её id.')
async def get_category(
    response: Response, 
    category_id: int) -> JSONResponse:

    category = category_orm.select_item_by_id(item_id=category_id)
    if category != {'message': 'Not found.'}:
        return JSONResponse(content=category, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No category found with the given ID.")


@router.post("/", summary='Создание новой категории товаров.')
async def create_category(
    response: Response, 
    category_data: CategoryData, 
    current_user: dict = Depends(get_current_user)) -> JSONResponse:

    if not await check_role(user_role=current_user['role'], allowed_roles=['admin', 'manager']):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=ACCESS_DENIED_MESSAGE)
    
    category = category_orm.add_category(name=category_data.name)
    if category['success'] == True:
        return JSONResponse(content=category, status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content=category, status_code=status.HTTP_409_CONFLICT)


@router.delete("/{category_id}", summary='Удаление категории товаров.')
async def delete_category(
    response: Response, 
    category_id: int, 
    current_user: dict = Depends(get_current_user)) -> JSONResponse:

    if not await check_role(user_role=current_user['role'], allowed_roles=['admin', 'manager']):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=ACCESS_DENIED_MESSAGE)
    
    category_orm.remove_item_by_id(item_id=category_id)
    return JSONResponse(content=f'Category (id = {category_id}) successfully deleted', status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{category_id}", summary='Обновление категории товаров.')
async def update_category(
    response: Response, 
    category_id: int, 
    category_data: CategoryData, 
    current_user: dict = Depends(get_current_user)) -> JSONResponse:
    
    if not await check_role(user_role=current_user['role'], allowed_roles=['admin', 'manager']):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=ACCESS_DENIED_MESSAGE)
    
    message = category_orm.update_category_name(category_id=category_id, category_name=category_data.name)

    if message['success'] == True:
        return JSONResponse(content=message, status_code=status.HTTP_204_NO_CONTENT)
    else:
        return JSONResponse(content=message, status_code=status.HTTP_409_CONFLICT)