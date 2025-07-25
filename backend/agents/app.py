from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from PIL import Image
import io
from crop_disease_agent.photo_agent import call_agent_image_analyzer
import json

app = FastAPI()


@app.post("/analyze_crop_disease")
async def analyze_crop_disease(image_file: UploadFile, location: str = Form(...)):
    try:
        image_data = await image_file.read()
        image = Image.open(io.BytesIO(image_data))

        result = call_agent_image_analyzer(image, location)
        print(result)

        cleaned_string = result.strip()

        if cleaned_string.startswith("```json"):
            cleaned_string = cleaned_string[len("```json"):].strip()

        if cleaned_string.endswith("```"):
            cleaned_string = cleaned_string[:-3].strip()
        try:
            data = json.loads(cleaned_string)
            print(data)
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
        return JSONResponse(content={"status": "success", "report": data})

    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)})

