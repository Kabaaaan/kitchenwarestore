from fastapi import APIRouter, Query, Response, Depends, status, HTTPException, UploadFile
from fastapi.responses import JSONResponse, FileResponse

from api.v1.schemas.schemas import *
from utils.auth import *
from database.models.models import Product, ProductImages
from utils.helpers import decimal_to_float
from decimal import Decimal

from api.v1.endpoints.users import get_current_user
from api.api_config import *

import os
from PIL import Image


router = APIRouter()
product_orm = Product()
images_orm = ProductImages()


@router.get("/", summary='Получение списка всех продуктов.')
async def get_products(
    response: Response,
    skip: int = Query(default=0, description="Number of items to skip", ge=0)) -> JSONResponse:
    
    products = product_orm.select_all()
    products = decimal_to_float(products)
    
    content = {
        'Count': len(products),
        'Products': products
    }

    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


@router.get("/{product_id}", summary='Получение продукта по его ID.')
async def get_product(
    response: Response, 
    product_id: int) -> JSONResponse:

    product = product_orm.select_item_by_id(item_id=product_id)
    for key, value in product.items():
        if isinstance(value, Decimal):
            product[key] = float(value)
    return JSONResponse(status_code=status.HTTP_200_OK, content=product)


@router.post("/", summary='Создание продукта.')
async def create_product(
    response: Response, 
    data: ProductDataToAdd, 
    current_user: dict = Depends(get_current_user)) -> JSONResponse:

    if not await check_role(user_role=current_user['role'], allowed_roles=['admin', 'manager']):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=ACCESS_DENIED_MESSAGE)
    
    product = product_orm.add_product(name=data.name,
                                        description=data.description,
                                        price=data.price,
                                        category_id=data.category_id,
                                        brand_id=data.brand_id)
    if product['success'] == True:
        return JSONResponse(content=product, status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content=product, status_code=status.HTTP_409_CONFLICT)


@router.delete("/{product_id}", summary='Удаление продукта по его ID.')
async def delete_product(
    response: Response, 
    product_id: int, 
    current_user: dict = Depends(get_current_user)) -> JSONResponse:

    if not await check_role(user_role=current_user['role'], allowed_roles=['admin', 'manager']):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=ACCESS_DENIED_MESSAGE)

    for ext in IMAGE_EXTENSIONS:
        file_path = IMAGES_DIR / f"{product_id}{ext}"
        if file_path.exists():
            os.remove(file_path)
            images_orm.remove_image(product_id=product_id)

    product_orm.remove_item_by_id(item_id=product_id)

    return JSONResponse(content=f'Product (id = {product_id}) successfully deleted', status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{product_id}", summary='Обновление продукта по его ID.')
async def update_product(
    response: Response, 
    product_id: int, 
    data: ProductDataToUpdate,
    current_user: dict = Depends(get_current_user)) -> JSONResponse:

    if not await check_role(user_role=current_user['role'], allowed_roles=['admin', 'manager']):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=ACCESS_DENIED_MESSAGE)
    
    product = product_orm.update_product(item_id=product_id,
                                            name=data.name,
                                            description=data.description,
                                            price=data.price,
                                            category_id=data.category_id,
                                            brand_id=data.brand_id)
    if product['success'] == True:
        return JSONResponse(content=product, status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content=product, status_code=status.HTTP_409_CONFLICT)


@router.get("/filter/category/{category_id}", summary='Получение списка продуктов категории по ID категории.')
async def get_products_by_category(
    response: Response,
    category_id: int,
    skip: int = Query(default=0, description="Number of items to skip", ge=0),  
    limit: int = Query(default=20, description="Number of items to return", ge=2)) -> JSONResponse:

    category_filter = product_orm.filter_by_row(row='category_id', row_value=category_id)
    category_filter = decimal_to_float(category_filter)
    paginated_products = category_filter[skip : skip + limit]

    content = {
        'Count': len(paginated_products),
        'Skip': skip,
        'Limit': limit,
        'Products': paginated_products
    }

    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


@router.get("/filter/brand/{brand_id}", summary='Получение списка продуктов бренда по ID бренда.')
async def get_products_by_brand(
    response: Response,
    brand_id: int,
    skip: int = Query(default=0, description="Number of items to skip", ge=0),  
    limit: int = Query(default=20, description="Number of items to return", ge=2)) -> JSONResponse:

    brand_filter = product_orm.filter_by_row(row='brand_id', row_value=brand_id)
    brand_filter = decimal_to_float(brand_filter)
    paginated_products = brand_filter[skip : skip + limit]

    content = {
        'Count': len(paginated_products),
        'Skip': skip,
        'Limit': limit,
        'Products': paginated_products
    }

    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


@router.get("/filter/both/{category_id}/{brand_id}", summary='Получение спсика продуктов бренда и категории по их ID.')
async def get_similar_products(
    response: Response, 
    category_id: int, 
    brand_id: int) -> JSONResponse:

    limit = 3
    category_filter = product_orm.filter_by_row(row='category_id', row_value=category_id)
    category_filter = decimal_to_float(category_filter)
    brand_filter = product_orm.filter_by_row(row='brand_id', row_value=brand_id)
    brand_filter = decimal_to_float(brand_filter)
    products_filter = [item for item in category_filter if item in brand_filter]
    paginated_products = products_filter[:limit]

    content = {
        'Count': len(paginated_products),
        'Limit': limit,
        'Products': paginated_products
    }

    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


@router.get('/image/{id}', summary='Получение фотографии продукта по его ID.')
async def get_product_image(
    response: Response, 
    id: int) -> FileResponse:

    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"

    try:
        print(f"Request received for id: {id}")
        for ext in IMAGE_EXTENSIONS:
            file_path = IMAGES_DIR / f"{id}{ext}"
            print(f"Checking file: {file_path}")
            if file_path.exists():
                return FileResponse(file_path, status_code=status.HTTP_200_OK)
        
        return FileResponse(PLACEHOLDER_PATH)
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/image/{product_id}", summary='удаление фотографии продукта по его ID.')
async def delete_image(
    response: Response, 
    product_id: int,
    current_user: dict = Depends(get_current_user)) -> JSONResponse:

    if not await check_role(user_role=current_user['role'], allowed_roles=['admin', 'manager']):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=ACCESS_DENIED_MESSAGE)
    
    for ext in IMAGE_EXTENSIONS:
        file_path = IMAGES_DIR / f"{product_id}{ext}"
        if file_path.exists():
            os.remove(file_path)
            images_orm.remove_image(product_id=product_id)
            return JSONResponse(content=f"File {product_id}{ext} deleted successfully", status_code=status.HTTP_204_NO_CONTENT)
    
    raise HTTPException(status_code=404, detail="File not found")


@router.post("/image/upload/{product_id}", summary='Загрузка фотографии продукта по его ID.')
async def upload_image(
    response: Response,
    product_id: int,
    file: UploadFile,
    current_user: dict = Depends(get_current_user)) -> JSONResponse:

    if not await check_role(user_role=current_user['role'], allowed_roles=['admin', 'manager']):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=ACCESS_DENIED_MESSAGE)

    for ext in IMAGE_EXTENSIONS:
        file_path = IMAGES_DIR / f"{product_id}{ext}"
        if file_path.exists():
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail='Already created.')
    
    try:
        image = images_orm.add_image(product_id=product_id)
        ext = os.path.splitext(file.filename)[1]
        original_file_path = IMAGES_DIR / f"{product_id}_original{ext}"
        with open(original_file_path, "wb") as buffer:
            buffer.write(file.file.read())
        
        image = Image.open(original_file_path)
        resized_image = image.resize((400, 400))
        resized_file_path = IMAGES_DIR / f"{product_id}{ext}"
        resized_image.save(resized_file_path)
        
        os.remove(original_file_path) 
        
        return JSONResponse(content='Image upload successfully', status_code=status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse(content=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@router.put("/image/update/{product_id}", summary='Обновление фотографии продукта по его ID.')
async def update_image(
    response: Response,
    product_id: int,
    file: UploadFile,
    current_user: dict = Depends(get_current_user)) -> JSONResponse:

    if not await check_role(user_role=current_user['role'], allowed_roles=['admin', 'manager']):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=ACCESS_DENIED_MESSAGE)
    
    try:

        for ext in IMAGE_EXTENSIONS:
            file_path = IMAGES_DIR / f"{product_id}{ext}"
            if file_path.exists():
                os.remove(file_path)
                ext = os.path.splitext(file.filename)[1]
                with open(file_path, "wb") as buffer:
                    buffer.write(file.file.read())
        
                    image = Image.open(file_path)
                    resized_image = image.resize((400, 400))
                    resized_image.save(file_path)
        
        return JSONResponse(content='Image updated successfully', status_code=status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse(content=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)