from fastapi import APIRouter, HTTPException, Response, Depends, status
from fastapi.responses import JSONResponse
from api.v1.endpoints.users import get_current_user

from api.v1.schemas.schemas import *
from api.api_config import *
from utils.auth import *
from database.models.models import Brand


router = APIRouter()
brands_orm = Brand()

@router.get("/", summary='Получение списка брендов.')
async def get_brands(response: Response) -> JSONResponse:
    brands = brands_orm.select_all()

    if len(brands) != 0:
        response_data = {'Count': len(brands), 'brands': brands}
        return JSONResponse(content=response_data, status_code=status.HTTP_200_OK)
    else: 
        return JSONResponse(content='No brands found.', status_code=status.HTTP_404_NOT_FOUND)


@router.get("/{brand_id}", summary='Получение бренда по его id.')
async def get_brand(
    response: Response, 
    brand_id: int) -> JSONResponse:

    brand = brands_orm.select_item_by_id(item_id=brand_id)
    if brand != {'message': 'Not found.'}:
        return JSONResponse(content=brand, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No brand found with the given ID.")


@router.post("/", summary='Создание нового бренда.')
async def create_brand(
    response: Response, 
    brand_data: BrandData, 
    current_user: dict = Depends(get_current_user)) -> JSONResponse:

    if not await check_role(user_role=current_user['role'], allowed_roles=['admin', 'manager']):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=ACCESS_DENIED_MESSAGE)
    
    brand = brands_orm.add_brand(name=brand_data.name)
    if brand['success'] == True:
        return JSONResponse(content=brand, status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content=brand, status_code=status.HTTP_409_CONFLICT)


@router.delete("/{brand_id}", summary='Удаление бренда.')
async def delete_brand(
    response: Response,
    brand_id: int, 
    current_user: dict = Depends(get_current_user)) -> JSONResponse:

    if not await check_role(user_role=current_user['role'], allowed_roles=['admin', 'manager']):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=ACCESS_DENIED_MESSAGE)
    
    brands_orm.remove_item_by_id(item_id=brand_id)
    return JSONResponse(content=f'Brand (id = {brand_id}) successfully deleted', status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{brand_id}", summary='Обновление бренда')
async def update_brand(
    response: Response, 
    brand_id: int, 
    brand_data: BrandData, 
    current_user: dict = Depends(get_current_user)) -> JSONResponse:
    
    if not await check_role(user_role=current_user['role'], allowed_roles=['admin', 'manager']):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=ACCESS_DENIED_MESSAGE)
    
    message = brands_orm.update_brand_name(brand_id=brand_id, brand_name=brand_data.name)

    if message['success'] == True:
        return JSONResponse(content=message, status_code=status.HTTP_204_NO_CONTENT)
    else:
        return JSONResponse(content=message, status_code=status.HTTP_409_CONFLICT)