from fastapi import FastAPI, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from repositories import OrderRepo, FoodRepo, MenuRepo, PaymentRepo
import schemas

app = FastAPI()

models.Base.metadata.create_all(bind=engine)  # will create our foodCourt.db tables and columns [10-4]


# @app.get("/")
# async def create_database():
#     return {"Database": "Created"}  # till now by running uvicorn, foodCourt.db will create automatically in the path.


# [11-1] Get all order from database
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# The reason wee created the DB with a try and finally is that whether(or not) we get a DB instance or session. and
# we always close the database.


# Read All Orders
@app.get("/", tags=["Order"])
async def read_all_order(db: Session = Depends(get_db)):
    return db.query(models.Order).all()


# find Order with primary-key(id)
@app.get("/order/{order_id}", tags=["Order"])
async def read_order(order_id: int, db: Session = Depends(get_db)):
    # food_model = db.query(models.Order).filter(models.Order.id == order_id).first()
    food_model = OrderRepo.fetch_by_id(db, order_id)
    if food_model is not None:
        return food_model
    raise http_exception()


# Post Request (Order Project)
@app.post("/", tags=["Order"])
async def create_order(order: schemas.CreateOrder, db: Session = Depends(get_db)):
    """ Create new order in database """
    food_model = OrderRepo.fetch_by_title(db, order_title=order.title)
    if food_model:
        raise HTTPException(status_code=400, detail="Oops! Item already exists!")  # whether order already exists or not
    await OrderRepo.create_order(db=db, order=order)

    return successful_response(201)


@app.put("/{order_id}", tags=["Order"])
async def update_order(order_id: int, order: schemas.Order, db: Session = Depends(get_db)):
    food_model = OrderRepo.fetch_by_id(db, order_id)

    if food_model is None:
        raise http_exception()

    update_item_encoded = jsonable_encoder(order)
    food_model.title = update_item_encoded['title']
    food_model.description = update_item_encoded['description']
    food_model.priority = update_item_encoded['priority']
    food_model.complete = update_item_encoded['complete']
    await OrderRepo.update(db=db, order_data=food_model)

    return successful_response(200)


# [11-5] Delete Request (Order Project)
@app.delete("/{order_id}", tags=["Order"])
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    food_model = OrderRepo.fetch_by_id(db, order_id)

    if food_model is None:
        raise http_exception()

    # db.query(models.Order).filter(models.Order.id == order_id).delete()
    # db.commit()
    await OrderRepo.delete(db, order_id)
    return successful_response(200)


# ---------------- Foods

# Read All Orders
@app.get("/foods", tags=["Food"])
async def read_all_food(db: Session = Depends(get_db)):
    return FoodRepo.fetch_all_food(db)  # see also previous read all


# find Food with primary-key(id)
@app.get("/foods/{food_id}", tags=["Food"])
async def read_food(food_id: int, db: Session = Depends(get_db)):
    food_model = FoodRepo.fetch_by_id(db, food_id)
    if food_model is not None:
        return food_model
    raise http_exception()


# Post Request (Order Project)
@app.post("/foods", tags=["Food"])
async def create_food(food: schemas.CreateFood, db: Session = Depends(get_db)):
    """ Create new order in database """
    food_model = FoodRepo.fetch_by_name(db, food_name=food.name)
    if food_model:
        raise HTTPException(status_code=400, detail="Oops! Item already exists!")  # whether order already exists or not
    await FoodRepo.create_food(db=db, food=food)

    return successful_response(201)


@app.put("/foods/{food_id}", tags=["Food"])
async def update_food(food_id: int, food: schemas.Food, db: Session = Depends(get_db)):
    food_model = FoodRepo.fetch_by_id(db, food_id)

    if food_model is None:
        raise http_exception()

    update_food_encoded = jsonable_encoder(food)
    food_model.name = update_food_encoded['name']
    food_model.image = update_food_encoded['image']
    food_model.description = update_food_encoded['description']
    food_model.price = update_food_encoded['price']
    food_model.rate = update_food_encoded['rate']
    food_model.country = update_food_encoded['country']
    await FoodRepo.update(db=db, food_data=food_model)

    return successful_response(200)


@app.delete("/foods/{food_id}", tags=["Food"])
async def delete_order(food_id: int, db: Session = Depends(get_db)):  # Check Previous for Different Approaches
    """ Delete Request From Database """
    food_model = FoodRepo.fetch_by_id(db, food_id)

    if food_model is None:
        raise http_exception()

    await FoodRepo.delete(db, food_id)
    return successful_response(200)


# -------------- Menu


@app.get("/menus", tags=["Menu"])
async def read_all_menus(db: Session = Depends(get_db)):
    """ Read All Menus """
    return MenuRepo.fetch_all_menus(db)  # see also previous read all


@app.get("/menus/{menu_id}", tags=["Menu"])
async def read_menu(menu_id: int, db: Session = Depends(get_db)):
    """ Find Menu with primary-key(id) """

    food_model = MenuRepo.fetch_by_id(db, menu_id)
    if food_model is not None:
        return food_model
    raise http_exception()


@app.post("/menus/", tags=["Menu"])
async def create_menu(menu: schemas.CreateMenu, db: Session = Depends(get_db)):
    """ Create new menu in database """
    food_model = MenuRepo.fetch_by_category(db, menu_category=menu.category)
    if food_model:
        raise HTTPException(status_code=400, detail="Oops! Item already exists!")
    await MenuRepo.create_menu(db=db, menu=menu)

    return successful_response(201)


@app.put("/menus/{menu_id}", tags=["Menu"])
async def update_menu(menu_id: int, menu: schemas.MenuBase, db: Session = Depends(get_db)):
    """ Updating the menu details """
    food_model = MenuRepo.fetch_by_id(db, menu_id)

    if food_model is None:
        raise http_exception()

    update_food_encoded = jsonable_encoder(menu)
    food_model.details = update_food_encoded['details']
    food_model.category = update_food_encoded['category']
    await MenuRepo.update(db=db, menu_data=food_model)

    return successful_response(200)


@app.delete("/menus/{menu_id}", tags=["Menu"])
async def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    """ Delete Request From Database """
    food_model = MenuRepo.fetch_by_id(db, menu_id)

    if food_model is None:
        raise http_exception()

    await MenuRepo.delete(db, menu_id)
    return successful_response(200)


# ----------- Payment


@app.get("/payment", tags=["Payment"])
async def read_all_payments(db: Session = Depends(get_db)):
    """ Read All Pays """
    return PaymentRepo.fetch_all_pays(db)


@app.get("/payment/{pay_id}", tags=["Payment"])
async def read_pays(pay_id: int, db: Session = Depends(get_db)):
    """ Find pays with primary-key(id) """

    pay_model = PaymentRepo.fetch_by_id(db, pay_id)
    if pay_model is not None:
        return pay_model
    raise http_exception()


# [10-3] Create new payment
@app.post("/payment/", tags=["Payment"])
async def create_payment(payment: schemas.CreatePayment, db: Session = Depends(get_db)):
    """ Create new payment in database """
    pay_model = PaymentRepo.fetch_by_bank_name(db, bank=payment.bank)
    if pay_model:
        raise HTTPException(status_code=400, detail="Oops! Item already exists!")
    await PaymentRepo.create_payment(db=db, payment=payment)

    return successful_response(201)


@app.put("/payment/{pay_id}", tags=["Payment"])
async def update_payment(pay_id: int, payment: schemas.PaymentBase, db: Session = Depends(get_db)):
    """ Updating the Payment details """
    pay_model = PaymentRepo.fetch_by_id(db, pay_id)

    if pay_model is None:
        raise http_exception()

    update_food_encoded = jsonable_encoder(payment)
    pay_model.bank = update_food_encoded['bank']
    pay_model.date = update_food_encoded['date']
    await PaymentRepo.update(db=db, payment_data=pay_model)

    return successful_response(200)


# [12-1] Delete payments
@app.delete("/payment/{pay_id}", tags=["Payment"])
async def delete_payment(pay_id: int, db: Session = Depends(get_db)):
    """ Delete Request From Database """
    food_model = PaymentRepo.fetch_by_id(db, pay_id)

    if food_model is None:
        raise http_exception()

    await PaymentRepo.delete(db, pay_id)
    return successful_response(200)


# -------------- Http Exception and Responses

def successful_response(status_code: int):
    return {
        "status": status_code,
        "transaction": "Successful"
    }


# creating a function for http_exception [11-2] useful for re-usability
def http_exception():
    return HTTPException(status_code=404, detail="Item not found !")
