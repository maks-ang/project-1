from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return ("Hello World!")

@app.get("/cat")
async def get_cat():
    return RedirectResponse("https://cataas.com/cat")
