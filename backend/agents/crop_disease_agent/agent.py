import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent, LlmAgent, SequentialAgent
from google.adk.tools import google_search
import google.genai as genai
from PIL import Image



def crop_disease_analyzer(image_path: str) -> dict:
    """
    Analyzes an image of a plant to identify potential diseases.
    """
    try:
        client = genai.Client( 
            vertexai=True,
            project="kisan-466906",
            location="global")

        image = Image.open(r"E:\Project_kisan\Agents\backend\agents\crop_disease_agent\plant.jpg")
        image.show()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[image, "Identify the plant disease from the photo"]
        )
        print(response.text)
        return {"status": "success", "report": response.text}
    except FileNotFoundError:
        return {
            "status": "error",
            "error_message": f"Could not find the image at '{image_path}'.",
        }
    except Exception as e:
        return {"status": "error", "error_message": f"An error occurred: {e}"}


disease_agent = LlmAgent(
    name="crop_disease_agent",
    model="gemini-2.0-flash",
    description="Agent that identifies plant disease from a photo.",
    instruction=(
        "You are an agricultural assistant. Use the crop_disease_analyzer tool "
        "to analyze the user-provided plant image and identify the disease. "
        "Return ONLY the disease name in a concise format."
    ),
    tools=[crop_disease_analyzer],
    output_key="disease_name",  # Important: this will be passed to next agent
)

# Agent 2: Finds remedies for the identified disease using Google search
remedies_agent = LlmAgent(
    name="crop_remedies_agent",
    model="gemini-2.0-flash",
    description="Agent that searches for remedies based on disease name.",
    instruction=(
        "You are an agricultural assistant. The user has a plant with the disease:. "
        "Use Google Search to find three effective remedies or treatments for this disease. "
        "Present them clearly and concisely."
    ),
    tools=[google_search],
    output_key="remedies_found"
)

# Main sequential agent
main_final_agent = SequentialAgent(
    name="Final_agent_1",
    sub_agents=[disease_agent, remedies_agent],
    description="An assistant that first diagnoses plant diseases from photos and then suggests remedies."
)

# Root agent for app
root_agent = main_final_agent
