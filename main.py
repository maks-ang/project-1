from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from routers.applications import router


app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(router)


templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request=request,name="index.html", context={})
@app.get("/cat")
async def get_cat():
    return RedirectResponse("https://cataas.com/cat")
