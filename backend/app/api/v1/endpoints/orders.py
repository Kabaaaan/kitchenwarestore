from fastapi import APIRouter, Response, Depends, status
from fastapi.responses import JSONResponse

from api.v1.schemas.schemas import *
from api.api_config import *
from utils.auth import *
from database.models.models import Order, OrderItem
from utils.helpers import decimal_to_float

from api.v1.endpoints.users import get_current_user

router = APIRouter()
order_orm = Order()
order_item_orm = OrderItem()

@router.get("/", summary='Получение всех заказов.')
async def get_orders(
    response: Response):
    
    orders = order_orm.select_all()
    orders = decimal_to_float(orders)

    if len(orders) != 0:
        response_data = {'Count': len(orders), 'Orders': orders}
        return JSONResponse(content=response_data, status_code=status.HTTP_200_OK)
    else: 
        return JSONResponse(content='No orders found.', status_code=status.HTTP_404_NOT_FOUND) 


@router.get("/{order_id}", summary='Получение всех элементов заказа.')
async def get_order(
    response: Response, 
    order_id: int) -> JSONResponse:

    order = order_item_orm.get_products_by_order_id(order_id=order_id)
    content = {'Count': len(order),
                'Products': order}
    return JSONResponse(status_code=status.HTTP_200_OK, content=content) 


@router.post('/', summary='Создание заказа.')
async def create_order(
    response: Response, 
    data: OrderDateToAdd):

    order = order_orm.add_order(user_id=data.user_id, total_price=data.total_price)
    if order['success']:
        return JSONResponse(status_code=status.HTTP_200_OK, content=order)
    else:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=order) 


@router.put('/{order_id}', summary='Обновление статуса заказа.')
async def update_order_status(
    response: Response, 
    order_id: int, 
    data: OrderDataToUpdate, 
    current_user: dict = Depends(get_current_user)) -> JSONResponse:

    if not await check_role(user_role=current_user['role'], allowed_roles=['admin', 'manager']):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=ACCESS_DENIED_MESSAGE)
    
    if data.status not in ['Done', 'In process']:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content='Invalid status. Must be "Done" or "In process".')
    order = order_orm.update_item_by_id(item_id=order_id, data={'status': data.status})
    if order['success']:
        return JSONResponse(status_code=status.HTTP_200_OK, content=order)
    else:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=order)


@router.post('/{order_id}/orderitem', summary='Добавление элемента заказа.')
async def add_order_item(
    response: Response, 
    order_id: int, 
    data: OrderItemData) -> JSONResponse:

    item = order_item_orm.add_order_item(order_id=order_id, product_id=data.product_id, quantity=data.quantity)
    if item['success']:
        return JSONResponse(status_code=status.HTTP_200_OK, content=item)
    else:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=item)