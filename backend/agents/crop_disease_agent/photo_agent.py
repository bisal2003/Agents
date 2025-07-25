import datetime
from zoneinfo import ZoneInfo
from google.adk.tools import google_search
import google.genai as genai
from google.genai import types
from PIL import Image
import base64
import os
from google import genai
from crop_disease_agent.prompts import MAIN_ANALYSIS_PROMPT



# crop_disease_analyzer_declaration = {
#     "name": "crop_disease_analyzer",
#     "description": "Analyzes an image of a plant to identify potential diseases.",
#     "parameters": {
#         "type": "object",
#         "properties": {
#             "image_path": {
#                 "type": "string",
#                 "description": "The path to the plant image to be analyzed for diseases.",
#             },
#         },
#         "required": ["image_path"],
#     },
# }

def crop_disease_analyzer(image: Image.Image) -> dict:
    """
    Analyzes an image of a plant to identify potential diseases.
    """
    try:
        client = genai.Client( 
            vertexai=True,
            project="kisan-466906",
            location="global")

        # image.show()
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=[image, "Identify the crop name and the plant disease from the photo and output that only"]
        )
        print(response.text)
        return {"status": "success", "report": response.text}
    except Exception as e:
        return {"status": "error", "error_message": f"An error occurred: {e}"}


def call_agent_image_analyzer(image : Image.Image, location : str):

    client = genai.Client( 
        vertexai=True,
        project="kisan-466906",
        location="global"
    )

    predict_disease = crop_disease_analyzer(image)
    print(predict_disease)

    final_text = MAIN_ANALYSIS_PROMPT.format(disease=predict_disease, location=location)

    model = "gemini-2.5-pro"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=final_text)
            ],
        ),
    ]
    tools = [
        types.Tool(googleSearch=types.GoogleSearch(
        )),
    ]
    generate_content_config = types.GenerateContentConfig(
        thinking_config = types.ThinkingConfig(
            thinking_budget=-1,
        ),
        tools=tools,
    )

    final_response = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")
        final_response += chunk.text

    return final_response



if __name__ == "__main__":
    location = "Assam"
    image = r"E:\Project_kisan\Agents\backend\agents\crop_disease_agent\plant.jpg"
    image = Image.open(image)
    # image.show()
    call_agent_image_analyzer(image, location)



# disease_agent = LlmAgent(
#     name="crop_disease_agent",
#     model="gemini-2.5-pro",
#     description="Agent that identifies plant disease from a photo.",
#     instruction=(
#         "You are an agricultural assistant. Use the crop_disease_analyzer tool "
#         "to analyze the user-provided plant image and identify the disease. "
#         "Return ONLY the disease name in a concise format."
#     ),
#     tools=[crop_disease_analyzer],
#     output_key="disease_name",  
# )

# remedies_agent = LlmAgent(
#     name="crop_remedies_agent",
#     model="gemini-2.5-pro",
#     description="Agent that searches for remedies based on disease name.",
#     instruction=(
#         "You are an agricultural assistant. The user has a plant with the disease: {disease_name}."
#         "Use Google Search to find three effective remedies or treatments for this disease. "
#         "Present them clearly and concisely."
#     ),
#     tools=[google_search],
#     output_key="remedies_found"
# )

# # Main sequential agent
# main_final_agent = SequentialAgent(
#     name="Final_agent_1",
#     sub_agents=[disease_agent, remedies_agent],
#     description="An assistant that first diagnoses plant diseases from photos and then suggests remedies."
# )

# # Root agent for app
# root_agent = main_final_agent


