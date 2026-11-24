from typing import Literal, Annotated
from fastapi import Depends, APIRouter, HTTPException, Path, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from model import Application
from schemas import CreateSchema, ReadSchema, StatusUpdateSchema

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("", status_code=201, response_model=ReadSchema)
def post_application(data: CreateSchema, db: Session = Depends(get_db), ):
    application = Application(customer_name=data.customer_name, phone=data.phone, email=data.email,
                              order_details=data.order_details)
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


@router.get("/{application_id}", response_model=ReadSchema)
def get_application(application_id: int = Path(gt=0), db: Session = Depends(get_db)):
    application = db.get(Application, application_id)
    if application is None:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    return application


@router.get("", response_model=list[ReadSchema])
def get_applications(status: Literal["new", "processing", "done"] | None = None, order: Literal["asc", "desc"] = "asc",
                     limit: Annotated[int, Query(ge=1, le=100)] = 20,
                     db: Session = Depends(get_db)):
    statement = select(Application)
    if status is not None:
        statement = statement.where(Application.status == status)
    if order == "asc":
        statement = statement.order_by(Application.id.asc())
    else:
        statement = statement.order_by(Application.id.desc())
    statement = statement.limit(limit)
    applications = db.scalars(statement).all()
    return applications


@router.patch("/{application_id}/status", response_model=ReadSchema)
def patch_application(data: StatusUpdateSchema, application_id: int = Path(gt=0), db: Session = Depends(get_db)):
    application = db.get(Application, application_id)
    if application is None:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    if application.status == data.status:
        return application
    allowed_status = {"new": {"processing"}, "processing": {"done"}, "done": set()}
    if data.status not in allowed_status[application.status]:
        raise HTTPException(status_code=409, detail="Недопустимая смена статуса")
    application.status = data.status
    db.commit()
    db.refresh(application)
    return application
