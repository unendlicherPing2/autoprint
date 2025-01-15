from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import subprocess

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

def build_model(diameter: float):
    subprocess.run(["./lib/FreeCAD_1.0.0/bin/freecadcmd.exe", "build_model.py", str(diameter)])

def slice_model():
    subprocess.run(["./lib/PrusaSlicer-2.9.0/prusa-slicer-console.exe",
        "--export-gcode",
        "--load", "", # // config.ini
        "--output", "./static/temp/biotop.gcode", 
        "./static/temp/floor.step", "./static/temp/body.step"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)