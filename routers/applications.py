from fastapi import Depends, APIRouter, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from database import get_db
from model import Application


router = APIRouter()


@router.post("/applications")
def create_application(
        customer_name: str = Form(),
        phone: str = Form(),
        order_details: str = Form(),
        db: Session = Depends(get_db),
):
    application = Application(customer_name=customer_name, phone=phone, order_details=order_details)
    db.add(application)
    db.commit()
    db.refresh(application)
    return RedirectResponse("/", status_code=303)
