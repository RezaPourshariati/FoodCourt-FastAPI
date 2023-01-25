from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from database import Base


# [12-4] Create database table for users
class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    order = relationship("Order", back_populates="owner")


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)  # index is for auto-increment id number
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("Users", back_populates="order")
    food = relationship("Food", back_populates="order")
    payment = relationship("Payment", back_populates="order")


class Food(Base):
    __tablename__ = "food"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    image = Column(String)
    description = Column(String)
    price = Column(Float)
    rate = Column(Float, default=0)
    country = Column(String)
    for_order = Column(Integer, ForeignKey("order.id"))

    order = relationship("Order", back_populates="food")
    menu = relationship("Menu", back_populates="food")


class Menu(Base):
    __tablename__ = "menu"

    menu_id = Column(Integer, primary_key=True, index=True)
    details = Column(String)
    category = Column(String)
    for_food = Column(Integer, ForeignKey("food.id"))

    food = relationship("Food", back_populates="menu")


class Payment(Base):
    __tablename__ = "payment"

    pay_id = Column(Integer, primary_key=True, index=True)
    bank = Column(String, default=None)
    date = Column(String)
    for_order = Column(Integer, ForeignKey("order.id"))

    order = relationship("Order", back_populates="payment")
