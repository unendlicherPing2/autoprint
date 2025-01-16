from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import subprocess
import requests
from requests.auth import HTTPDigestAuth

PRUSA_CONNECT_API = "https://connect.prusa3d.com"
PRUSA_CONNECT_API_KEY = ""
PRINTER_TARGET_PATH = "/autoprint/"
PRINTER_ID = ""
FILE_PATH = "./static/temp/biotop.gcode"

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html", media_type="text/html")

@app.post("/generate")
async def generate(diameter: float = Form(...)):
    build_model(diameter)
    slice_model()
    return FileResponse("static/generate.html", media_type="text/html")

@app.get("/upload")
async def upload():
    print(upload_gcode().content)
    return FileResponse("static/index.html", media_type="text/html")

def build_model(diameter: float):
    subprocess.run(["./lib/FreeCAD_1.0.0/bin/freecadcmd.exe", "build_model.py", str(diameter)])

def slice_model():
    subprocess.run(["./lib/PrusaSlicer-2.9.0/prusa-slicer-console.exe",
        "--export-gcode",
        "--load", "", # // config.ini
        "--output", "./static/temp/biotop.gcode", 
        "./static/temp/floor.step", "./static/temp/body.step"])

def upload_gcode() -> requests.Response:
    with open(FILE_PATH, "rb") as file:
        return requests.put(
            f"{PRUSA_CONNECT_API}/api/v1/printers/{PRINTER_ID}/files/",
            headers={
                "Authorization": f"Token {PRUSA_CONNECT_API_KEY}",
                "Content-Type": "application/octet-stream"
            },
            data=file
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
