import os
import shutil
import yaml
import json
import time

from http import HTTPStatus
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.func.load_model import LoadModel
from src.func.process import process_image, process_line


# Load base config
with open("cfg/base.yaml", 'r', encoding='utf-8') as stream:
    cfg_base = yaml.safe_load(stream)


# Load models
models = LoadModel(cfg_base)


# Initialize FastAPI app
app = FastAPI(
    title="OCR",
    description="API to process and extract information from document images using OCR technology.",
    version="1.0.0"
)

# Mount static files (uploads folder)
upload_folder = "uploads"
os.makedirs(upload_folder, exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


# Set up template directory
templates = Jinja2Templates(directory="templates")


# Check allowed extensions
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}


def allowed_file(filename: str):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Route for index page
@app.get("/", response_class=FileResponse, include_in_schema=False, tags=["Passport Reader"])
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Route for web Demo
@app.post("/", include_in_schema=False, tags=["Passport Reader"])
async def upload_file(file: UploadFile = File(...), request: Request = None):
    if file.filename == '':
        return {"error": "No file selected"}

    if allowed_file(file.filename):
        file_location = f"{upload_folder}/{file.filename}"

        # Save file to uploads directory
        with open(file_location, "wb+") as f:
            shutil.copyfileobj(file.file, f)

        # Process the image using the AI model
        start_time = time.time()
        result = process_image(models, file_location)
        execution_time = round(time.time() - start_time, 5)

        return templates.TemplateResponse("result.html", {
            "request": request,
            "image_url": f"/uploads/{file.filename}",
            "result_info": result,
            "execution_time": execution_time
        })
    else:
        return {"error": "Invalid file type"}


# Route for API
@app.post("/reader", tags=["Test"])
async def upload_a_line(file: UploadFile = File(...), request: Request = None):
    payload = {
        "status": HTTPStatus.OK,
        "error": False,
        "msg": "success",
        "data": {}
    }

    if file.filename == '':
        payload["status"] = HTTPStatus.BAD_REQUEST
        payload["error"] = True
        payload["msg"] = "No file selected"
        return payload

    if allowed_file(file.filename):
        file_location = f"{upload_folder}/{file.filename}"

        # Save file to uploads directory
        with open(file_location, "wb+") as f:
            shutil.copyfileobj(file.file, f)

        # Process the image using the AI model
        result = process_line(models, file_location)

        payload["data"] = json.loads(result)

        return payload
    else:
        payload["status"] = HTTPStatus.BAD_REQUEST
        payload["error"] = True
        payload["msg"] = "Invalid file type"
        return payload


# Route for API
@app.post("/passport", tags=["Passport Reader"])
async def upload_file_api(file: UploadFile = File(...), request: Request = None):
    payload = {
        "status": HTTPStatus.OK,
        "error": False,
        "msg": "success",
        "data": {}
    }

    if file.filename == '':
        payload["status"] = HTTPStatus.BAD_REQUEST
        payload["error"] = True
        payload["msg"] = "No file selected"
        return payload

    if allowed_file(file.filename):
        file_location = f"{upload_folder}/{file.filename}"

        # Save file to uploads directory
        with open(file_location, "wb+") as f:
            shutil.copyfileobj(file.file, f)

        # Process the image using the AI model
        result = process_image(models, file_location)

        payload["data"] = json.loads(result)

        return payload
    else:
        payload["status"] = HTTPStatus.BAD_REQUEST
        payload["error"] = True
        payload["msg"] = "Invalid file type"
        return payload
    

# Serve uploaded files
@app.get("/uploads/{filename}", include_in_schema=False, tags=["Passport Reader"])
async def uploaded_file(filename: str):
    file_path = os.path.join("uploads", filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8989)
