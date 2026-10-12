from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
from model import Application
from schemas import ApplicationCreate

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=engine)


@app.post("/applications")
def create_application(
        application_data: ApplicationCreate,
        db: Session = Depends(get_db),
):
    application = Application(**application_data.model_dump())
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


@app.get("/")
def home():
    return ("new text")

@app.get("/cat")
async def get_cat():
    return RedirectResponse("https://cataas.com/cat")
