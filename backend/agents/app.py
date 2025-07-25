from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from PIL import Image
import io
from crop_disease_agent.photo_agent import call_agent_image_analyzer


app = FastAPI()


@app.post("/analyze_crop_disease")
async def analyze_crop_disease(image_file: UploadFile, location: str = Form(...)):
    try:
        image_data = await image_file.read()
        image = Image.open(io.BytesIO(image_data))

        result = call_agent_image_analyzer(image, location)
        return JSONResponse(content={"status": "success", "report": result})

    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)})

