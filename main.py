from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import base64
import uvicorn
from clothing_description import ClothingDescription
import base64
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY-2")

app = FastAPI()

# Allow frontend requests (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve HTML static file
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def get_ui():
    with open("static/index.html", "r") as f:
        return f.read()


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    image_bytes = await file.read()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    # Call your custom image processing function here
    # result = your_image_processing_function(base64_image)
    result = infer_image_base64(base64_image)

    return JSONResponse(content=result)


def infer_image_base64(input_image_base64):
    # with open("something.txt", "r") as file:
    #     something = file.read()
    # file.close()

    with open('prompt.txt', 'r') as file:
        prompt = file.read()
    clothing_description = ClothingDescription(API_KEY)
    result = clothing_description.describe_clothing(input_image_base64, prompt)

    return result

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def your_image_processing_function(base64_img_str):
    # Replace this with your actual image processing logic


    return {
        "status": "success",
        "length_of_base64_string": len(base64_img_str),
        "summary": "Image processed successfully",
        "dummy_json_data": {
            "details": [f"Line {i}" for i in range(1, 101)]
        }
    }


# ✅ This is the part you asked about
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
