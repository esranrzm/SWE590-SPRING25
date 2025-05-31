from fastapi import FastAPI, HTTPException
import requests
from google.oauth2 import service_account
import google.auth.transport.requests
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import os
import time
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OUTPUT_DIR = "processed_images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

CLOUD_FUNCTION_URL = 'https://us-central1-swe590-project-458808.cloudfunctions.net/hello-esra'
SERVICE_ACCOUNT_FILE = './key.json'

credentials = service_account.IDTokenCredentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    target_audience=CLOUD_FUNCTION_URL
)

# Function to perform CPU-intensive image processing
def cpu_intensive_task(image: Image.Image) -> Image.Image:
    img_array = np.array(image)
    for _ in range(50):
        img_array = np.clip((img_array * 1.01), 0, 255)
    return Image.fromarray(img_array.astype('uint8'))

# Function to download and process an image
def download_and_process_image(index: int) -> str:
    response = requests.get("https://picsum.photos/512/512")
    if response.status_code != 200:
        return f"image_{index}_failed"

    image = Image.open(io.BytesIO(response.content)).convert("RGB")
    image = image.resize((256, 256)).convert("L")
    processed = cpu_intensive_task(image)

    filename = f"{int(time.time())}_img{index}.jpg"
    filepath = os.path.join(OUTPUT_DIR, filename)
    processed.save(filepath, format="JPEG", quality=80)
    return filename


@app.get("/api/hello")
async def proxy_hello():
    try:
        request = google.auth.transport.requests.Request()
        credentials.refresh(request)
        id_token = credentials.token

        response = requests.get(
            CLOUD_FUNCTION_URL,
            headers={'Authorization': f'Bearer {id_token}'}
        )
        response.raise_for_status()
        return response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Endpoint to trigger image processing
@app.get("/process")
def process_multiple_images():
    count = 2
    start_time = time.time()
    processed_files = []

    for i in range(count):
        filename = download_and_process_image(i)
        processed_files.append(filename)

    total_time = round(time.time() - start_time, 2)
    return {
        "status": "batch complete",
        "processed_images": processed_files,
        "total_images": len(processed_files),
        "total_time_sec": total_time,
        "avg_time_per_image_sec": round(total_time / len(processed_files), 2)
    }
