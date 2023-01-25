from pydantic import BaseModel, Field
from typing import Optional


class User(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str
    is_active = bool


class CreateUser(User):
    pass


class Order(BaseModel):
    # id:   -->   we will let the ORM handle all the ID auto-increments.
    title: str
    description: Optional[str]
    priority: int = Field(gt=0, lt=6, description="The priority must be between 1-5")
    complete: bool


class CreateOrder(Order):
    pass


class Food(BaseModel):
    name: str
    image: str
    description: Optional[str]
    price: float
    rate: float = Field(gt=0, lt=6, description="The rate of food must be between 1-5")
    country: str


class CreateFood(Food):
    pass


class MenuBase(BaseModel):
    details: str
    category: str


class CreateMenu(MenuBase):
    pass


class Menu(MenuBase):
    menu_id: int

    class Config:
        orm_mode: True


class PaymentBase(BaseModel):
    bank: str
    date: str


class CreatePayment(PaymentBase):
    pass
