from pydantic import BaseModel

class Credentials(BaseModel):
    name: str
    password: str

class UsersDataToUpdate(BaseModel):
    name: str | None = None
    password: str | None = None
    role: str | None = None

class BrandData(BaseModel):
    name: str

class CategoryData(BaseModel):
    name: str

class OrderDataToUpdate(BaseModel):
    status: str

class OrderDateToAdd(BaseModel):
    user_id: int
    total_price: float

class OrderItemData(BaseModel):
    product_id: int
    quantity: int

class ProductDataToAdd(BaseModel):
    name: str
    description: str
    price: float
    category_id: int
    brand_id: int

class ProductDataToUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    category_id: int | None = None
    brand_id: int | None = None

class ImageData(BaseModel):
    product_id: int
    image_alt: str