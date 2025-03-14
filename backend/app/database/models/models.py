from database.models.base_model import BaseModel
import sqlalchemy as db
from sqlalchemy.exc import IntegrityError, OperationalError
import typing


class User(BaseModel):
    def __init__(self, table_name: str = "User"):
        super().__init__(table_name)
        self.allowed_roles = {'admin', 'manager', 'regular'}

    def _validate_role(self, role: str) -> bool:
        return role in self.allowed_roles

    def add_user(self, name: str, password: str, role: str) -> dict:
        """
        Добавляет нового пользователя в базу данных.

        :param name: Имя пользователя.
        :param password: Пароль пользователя.
        :param role: Роль пользователя (например, 'admin', 'manager', 'regular').
        :return: Словарь с результатом операции.
        """
        if not self._validate_role(role):
            return {
                "success": False,
                "message": f'Error: Role "{role}" is not valid. Allowed roles are: {", ".join(self.allowed_roles)}.'
            }


        insert_query = self.table.insert().values(name=name, password=password, role=role)
        try:
            return self._execute_and_commit(insert_query)
        except OperationalError as e:
            self.connection = self.engine.connect()
            return self._execute_and_commit(insert_query)
        except IntegrityError as e:
            return {
                "success": False,
                "message": f'User name must be unique.'
            }

    def update_user_account(self, user_id: int, name: str = None, password: str = None, role: str = None) -> dict:
        """
        Обновляет учетную запись пользователя в базе данных.

        :param user_id: Идентификатор пользователя, чью учетную запись нужно обновить.
        :param name: Новое имя пользователя (необязательный параметр).
        :param password: Новый пароль пользователя (необязательный параметр).
        :param role: Новая роль пользователя (необязательный параметр).
        :return: Словарь с результатом операции.
        """
        if not any([name, password, role]):
            return {
                "success": False,
                "message": "Warning: At least one of the optional parameters (name, password, role) must be provided."
            }

        updates = {}
        if name is not None:
            updates['name'] = name
        if password is not None:
            updates['password'] = password
        if role is not None:
            if not self._validate_role(role):
                return {
                    "success": False,
                    "message": f'Error: Role "{role}" is not valid. Allowed roles are: {", ".join(self.allowed_roles)}.'
                }
            updates['role'] = role

        update_query = self.table.update().where(self.table.c.id == user_id).values(**updates)

        try:
            result = self._execute_query(update_query)
            self.commit()
            if result.rowcount == 0:
                return {
                    "success": False,
                    "message": "No user found with the given ID"
                }
            else:
                return {
                    "success": True,
                    "message": "User account successfully updated"
                }
        except Exception as e:
            self.connection.rollback()
            return {
                "success": False,
                "message": f"An error occurred: {str(e)}"
            }

        
class Category(BaseModel):
    def __init__(self, table_name: str = "Category"):
        super().__init__(table_name)

    def add_category(self, name: str) -> dict:
        """
        Добавляет новую категорию товаров в базу данных.

        :param name: Название категории.
        :return: Словарь с результатом операции.
        """
        check_query = self.table.select().where(self.table.c.name == name)
        existing_category = self._execute_query(check_query).fetchone()

        if existing_category:
            return {
                "success": False,
                "message": "Error: Category with this name already exists."
            }

        insert_query = self.table.insert().values(name=name)
        return self._execute_and_commit(insert_query)

    def update_category_name(self, category_id: int, category_name: str) -> dict:
        """
        Обновляет название категории товаров в базе данных.

        :param category_id: ID категории.
        :param category_name: Новое название категории.
        :return: Словарь с результатом операции.
        """
        existing_category = self.select_item_by_id(category_id)
        if not existing_category:
            return {
                "success": False,
                "message": "Error: No category found with the given ID."
            }

        update_query = self.table.update().where(self.table.c.id == category_id).values(name=category_name)

        try:
            self._execute_query(update_query)
            self.commit()
            return {
                "success": True,
                "message": "Category name successfully updated."
            }
        except Exception as e:
            self.connection.rollback()
            return {
                "success": False,
                "message": f"An error occurred: {str(e)}"
            }
        

class Brand(BaseModel):
    def __init__(self, table_name: str = "Brand"):
        super().__init__(table_name)

    def add_brand(self, name: str) -> dict:
        """
        Добавляет новый бренд в базу данных.

        :param name: Название бренда.
        :return: Словарь с результатом операции.
        """
        check_query = self.table.select().where(self.table.c.name == name)
        existing_brand = self._execute_query(check_query).fetchone()

        if existing_brand:
            return {
                "success": False,
                "message": "Error: Brand with this name already exists."
            }

        insert_query = self.table.insert().values(name=name)
        return self._execute_and_commit(insert_query)

    def update_brand_name(self, brand_id: int, brand_name: str) -> dict:
        """
        Обновляет название бренда в базе данных.

        :param brand_id: ID бренда.
        :param brand_name: Новое название бренда.
        :return: Словарь с результатом операции.
        """
        existing_brand = self.select_item_by_id(brand_id)
        if not existing_brand:
            return {
                "success": False,
                "message": "Error: No brand found with the given ID."
            }

        update_query = self.table.update().where(self.table.c.id == brand_id).values(name=brand_name)

        try:
            self._execute_query(update_query)
            self.commit()
            return {
                "success": True,
                "message": "Brand name successfully updated."
            }
        except Exception as e:
            self.connection.rollback()
            return {
                "success": False,
                "message": f"An error occurred: {str(e)}"
            }


class Product(BaseModel):
    def __init__(self, table_name: str = "Product"):
        super().__init__(table_name)

    def add_product(self, name: str, description: str, price: float, category_id: int, brand_id: int) -> dict:
        """
        Добавляет новый товар в базу данных.

        :param name: Название товара.
        :param description: Описание товара.
        :param price: Цена товара.
        :param category_id: ID категории товара.
        :param brand_id: ID бренда товара.
        :return: Словарь с результатом операции.
        """
        insert_query = self.table.insert().values(
            name=name,
            description=description,
            price=price,
            category_id=category_id,
            brand_id=brand_id
        )
        return self._execute_and_commit(insert_query)

    def update_product(self, item_id: int, name: str = None, description: str = None, 
                       price: float = None, category_id: int = None, brand_id: int = None) -> dict:
        """
        Обновляет информацию о товаре в базе данных.

        :param item_id: ID товара, который нужно обновить.
        :param name: Новое название товара (или None, если не нужно менять).
        :param description: Новое описание товара (или None, если не нужно менять).
        :param price: Новая цена товара (или None, если не нужно менять).
        :param category_id: Новый ID категории товара (или None, если не нужно менять).
        :param brand_id: Новый ID бренда товара (или None, если не нужно менять).
        :return: Словарь с результатом операции.
        """

        update_values = {}
        if name is not None:
            update_values['name'] = name
        if description is not None:
            update_values['description'] = description
        if price is not None:
            update_values['price'] = price
        if category_id is not None:
            update_values['category_id'] = category_id
        if brand_id is not None:
            update_values['brand_id'] = brand_id

        if not update_values:
            return {
                "success": False,
                "message": "No fields to update."
            }

        update_query = self.table.update().where(self.table.c.id == item_id).values(**update_values)

        try:
            result = self._execute_query(update_query)
            self.commit()
            if result.rowcount == 0:
                return {
                    "success": False,
                    "message": "No product found with the given ID."
                }
            else:
                return {
                    "success": True,
                    "message": "Product successfully updated."
                }
        except Exception as e:
            self.connection.rollback()
            return {
                "success": False,
                "message": f"An error occurred: {str(e)}"
            }


class ProductImages(BaseModel):
    def __init__(self, table_name: str = "ProductImages"):
        super().__init__(table_name)

    def add_image(self, product_id: int, image_alt: str = 'None') -> dict:
        """
        Добавляет новую фотографию в базу данных.

        :param product_id: ID товара.
        :param image_alt: Alt текст фотографии.
        :return: ID добавленной записи.
        """
        insert_query = self.table.insert().values(
            product_id=product_id,
            image_alt=image_alt
        )

        return self._execute_and_commit(insert_query)

    def update_image(self, image_id: int, image_alt: str = 'None') -> dict:
        """
        Обновляет информацию о фотографии в базе данных.

        :param image_id: ID фотографии, которую нужно обновить.
        :param image_alt: Новый alt текст фотографии (или None, если не нужно менять).
        :return: Словарь с результатом операции.
        """

        if not image_alt:
            return {
                "success": False,
                "message": "No fields to update."
            }

        update_query = self.table.update().where(self.table.c.product_id == image_id).values(image_alt=image_alt)

        try:
            result = self._execute_query(update_query)
            self.commit()
            if result.rowcount == 0:
                return {
                    "success": False,
                    "message": "No image found with the given ID."
                }
            else:
                return {
                    "success": True,
                    "message": "Image successfully updated."
                }
        except Exception as e:
            self.connection.rollback()
            return {
                "success": False,
                "message": f"An error occurred: {str(e)}"
            }
        
    def remove_image(self, product_id: int) -> None:
        remove_query = self.table.delete().where(self.table.c.product_id == product_id)
        self._execute_query(remove_query)
        self.commit()

    def select_item_by_id(self, item_id: int) -> dict:
        query = self.table.select().where(self.table.c.product_id == item_id)
        query_result = self._execute_query(query)
        result = self._format_result(query_result)
        if len(result) != 0:
            return result[0]
        else:
            return {'message': 'Not found.'}


class Order(BaseModel):
    def __init__(self, table_name: str = "Order"):
        super().__init__(table_name)

    def add_order(self, user_id: int, total_price: float, status='default') -> dict:
        """
        Добавляет новый заказ в базу данных.

        :param user_id: ID пользователя.
        :param total_price: Общая сумма заказа.
        :param status: Статус заказа (по умолчанию 'default').
        :return: Словарь с результатом операции.
        """
        insert_query = self.table.insert().values(user_id=user_id, total_price=total_price, status=status)
        return self._execute_and_commit(insert_query)


class OrderItem(BaseModel):
    def __init__(self, table_name: str = "OrderItem"):
        super().__init__(table_name)

    def add_order_item(self, order_id: int, product_id: int, quantity: int) -> dict:
        """
        Добавляет новый элемент заказа в базу данных.

        :param order_id: ID заказа.
        :param product_id: ID товара.
        :param quantity: Количество данных товаров в заказе.
        :return: Словарь с результатом операции.
        """
            
        insert_query = self.table.insert().values(order_id=order_id, product_id=product_id, quantity=quantity)
        return self._execute_and_commit(insert_query)
        

    def get_products_by_order_id(self, order_id: int) -> typing.List[dict]:
        """
        Получение списка всех товаров в заказе по id заказа.

        :param order_id: ID заказа.
        :return: Список товаров данного заказа.
        """
        query = db.select(self.table).where(self.table.c.order_id == order_id)

        try:
            query_result = self.connection.execute(query)
        except Exception as e:
            self.connection = self.engine.connect()
            query_result = self.connection.execute(query)

        return self._format_result(query_result)
    
    def select_item_by_id(self):
        return 'This class haven`t a method.'