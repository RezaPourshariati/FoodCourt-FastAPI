import sys

sys.path.append("..")

from starlette import status
from starlette.responses import RedirectResponse

from fastapi import Depends, APIRouter, Request, Form
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from .auth import get_current_user

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/orders",
    tags=["Order"],
    responses={404: {"description": "Not found"}}
)

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# ------------------- [17-18] Get all Orders by User
@router.get("/", response_class=HTMLResponse)
async def read_all_by_user(request: Request, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    orders = db.query(models.Order).filter(models.Order.owner_id == user.get("id")).all()

    return templates.TemplateResponse("home.html", {"request": request, "orders": orders, "user": user})


@router.get("/add-order", response_class=HTMLResponse)
async def add_new_order(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse("add-order.html", {"request": request, "user": user})


# ------------------- [17-19] Adding new Todos to our application
@router.post("/add-order", response_class=HTMLResponse)
async def create_order(request: Request, title: str = Form(...), description: str = Form(...),
                       priority: int = Form(...), db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    food_model = models.Order()
    food_model.title = title
    food_model.description = description
    food_model.priority = priority
    food_model.complete = False
    food_model.owner_id = user.get("id")

    db.add(food_model)
    db.commit()

    return RedirectResponse(url="/orders", status_code=status.HTTP_302_FOUND)


# ------------------- [17-20] Edit Todos
@router.get("/edit-order/{order_id}", response_class=HTMLResponse)
async def edit_order(request: Request, order_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    order = db.query(models.Order).filter(models.Order.id == order_id).first()

    return templates.TemplateResponse("edit-order.html", {"request": request, "order": order, "user": user})


# ------------------- [17-21] Edit Todos POST
@router.post("/edit-order/{order_id}", response_class=HTMLResponse)
async def edit_order_commit(request: Request, order_id: int, title: str = Form(...),
                            description: str = Form(...), priority: int = Form(...),
                            db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    food_model = db.query(models.Order).filter(models.Order.id == order_id).first()

    food_model.title = title
    food_model.description = description
    food_model.priority = priority

    db.add(food_model)
    db.commit()

    return RedirectResponse(url="/orders", status_code=status.HTTP_302_FOUND)


# ------------------- [17-22] Delete Todos
@router.get("/delete/{order_id}")
async def delete_order(request: Request, order_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    food_model = db.query(models.Order).filter(models.Order.id == order_id) \
        .filter(models.Order.owner_id == user.get("id")).first()  # verifying that the ID belongs to the user and valid.

    if food_model is None:
        return RedirectResponse(url="/orders", status_code=status.HTTP_302_FOUND)

    db.query(models.Order).filter(models.Order.id == order_id).delete()

    db.commit()

    return RedirectResponse(url="/orders", status_code=status.HTTP_302_FOUND)


# ------------------- [17-23] Complete Functionality
@router.get("/complete/{order_id}", response_class=HTMLResponse)
async def complete_order(request: Request, order_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    order = db.query(models.Order).filter(models.Order.id == order_id).first()

    order.complete = not order.complete

    db.add(order)
    db.commit()

    return RedirectResponse(url="/orders", status_code=status.HTTP_302_FOUND)
