from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# This tells FastAPI where to look for your HTML files
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    # This renders the index.html file inside your templates folder
    return templates.TemplateResponse(
    request=request, name="index.html", context={"title": "My FastAPI App"}
)


@app.get("/status")
def get_status():
    return {"status": "Terminal is running and Git is watching!"}
