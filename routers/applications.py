from fastapi import Depends, APIRouter, Form, HTTPException, Path
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Annotated

from database import get_db
from model import Application
from schemas import ApplicationCreate, ApplicationRead


router = APIRouter()


@router.post("/applications")
def create_application(data: Annotated[ApplicationCreate, Form()], db: Session = Depends(get_db),):
    application = Application(customer_name=data.customer_name, phone=data.phone, email=data.email, order_details=data.order_details)
    db.add(application)
    db.commit()
    db.refresh(application)
    return RedirectResponse("/", status_code=303)


@router.get("/applications/{application_id}", response_model=ApplicationRead)
def get_application(application_id: int = Path(gt=0), db: Session = Depends(get_db)):
    application = db.get(Application, application_id)
    if application is None:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    return application
