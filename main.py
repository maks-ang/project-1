from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get("/")
def home():
    return ("new text")

@app.get("/cat")
async def get_cat():
    return RedirectResponse("https://cataas.com/cat")
