from sqlalchemy.orm import Session
import models
import schemas


class OrderRepo:

    async def create_order(db: Session, order: schemas.Order):
        db_order = models.Order(title=order.title, description=order.description, priority=order.priority,
                                complete=order.complete)
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return db_order

    def fetch_by_id(db: Session, order_id):
        return db.query(models.Order).filter(models.Order.id == order_id).first()

    def fetch_by_title(db: Session, order_title):
        return db.query(models.Order).filter(models.Order.title == order_title).first()

    def fetch_all_order(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Order).offset(skip).limit(limit).all()

    async def delete(db: Session, order_id):
        db.query(models.Order).filter(models.Order.id == order_id).delete()
        db.commit()

    async def update(db: Session, order_data):
        updated_order = db.merge(order_data)
        db.commit()
        return updated_order


class FoodRepo:

    async def create_food(db: Session, food: schemas.CreateFood):
        db_food = models.Food(name=food.name, image=food.image, description=food.description,
                              price=food.price, rate=food.rate, country=food.country)
        db.add(db_food)
        db.commit()
        db.refresh(db_food)
        return db_food

    def fetch_by_id(db: Session, food_id):
        return db.query(models.Food).filter(models.Food.id == food_id).first()

    def fetch_by_name(db: Session, food_name):
        return db.query(models.Food).filter(models.Food.name == food_name).first()

    def fetch_all_food(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Food).offset(skip).limit(limit).all()

    async def delete(db: Session, food_id):
        db.query(models.Food).filter(models.Food.id == food_id).delete()
        db.commit()

    async def update(db: Session, food_data):
        updated_foods = db.merge(food_data)
        db.commit()
        return updated_foods


class MenuRepo:

    async def create_menu(db: Session, menu: schemas.CreateMenu):
        db_menu = models.Menu(details=menu.details, category=menu.category)
        db.add(db_menu)
        db.commit()
        db.refresh(db_menu)
        return db_menu

    def fetch_by_id(db: Session, menu_id):
        return db.query(models.Menu).filter(models.Menu.menu_id == menu_id).first()

    def fetch_by_category(db: Session, menu_category):
        return db.query(models.Menu).filter(models.Menu.category == menu_category).first()

    def fetch_all_menus(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Menu).offset(skip).limit(limit).all()

    async def delete(db: Session, menu_id):
        db.query(models.Menu).filter(models.Menu.menu_id == menu_id).delete()
        db.commit()

    async def update(db: Session, menu_data):
        updated_menus = db.merge(menu_data)
        db.commit()
        return updated_menus


class PaymentRepo:

    async def create_payment(db: Session, payment: schemas.CreatePayment):
        db_payment = models.Payment(bank=payment.bank, date=payment.date)
        db.add(db_payment)
        db.commit()
        db.refresh(db_payment)
        return db_payment

    def fetch_by_id(db: Session, pay_id):
        return db.query(models.Payment).filter(models.Payment.pay_id == pay_id).first()

    def fetch_by_bank_name(db: Session, bank):
        return db.query(models.Payment).filter(models.Payment.bank == bank).first()

    def fetch_all_pays(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Payment).offset(skip).limit(limit).all()

    async def delete(db: Session, pay_id):
        db.query(models.Payment).filter(models.Payment.pay_id == pay_id).delete()
        db.commit()

    async def update(db: Session, payment_data):
        updated_pays = db.merge(payment_data)
        db.commit()
        return updated_pays
