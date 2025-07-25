import os
from PIL import Image
import google.genai as genai
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools import FunctionTool, google_search


# -------------------------------
# 1. TOOL: Crop Disease Analyzer
# -------------------------------
def crop_disease_analyzer(image_path: str) -> dict:
    """
    Analyzes a plant image to detect diseases using Gemini model.

    Args:
        image_path (str): Path to the plant image.

    Returns:
        dict: { "status": "success"/"error", "disease_name": "Name of disease" }
    """
    try:
        if not os.path.exists(image_path):
            return {"status": "error", "error_message": f"Image not found at {image_path}"}

        client = genai.Client(
            vertexai=True,
            project="kisan-466906",  # ✅ Replace with your GCP project ID
            location="global"
        )

        image = Image.open(image_path)
        response = client.models.generate_content(
            model="gemini-2.5-flash",  # ✅ Change if required
            contents=[image, "Identify the plant disease from this photo. "
                            "Return ONLY the disease name (no explanation)."]
        )

        return {"status": "success", "disease_name": response.text.strip()}

    except Exception as e:
        return {"status": "error", "error_message": str(e)}


# Wrap as ADK tool
crop_disease_tool = FunctionTool(func=crop_disease_analyzer)


# -----------------------------------
# 2. Agent 1: Disease Detection Agent
# -----------------------------------
disease_agent = LlmAgent(
    name="crop_disease_agent",
    model="gemini-2.0-flash",  # ✅ Choose lightweight model for reasoning
    description="Identifies plant diseases from an image.",
    instructions=(
        "You are an agricultural assistant. "
        "Use the `crop_disease_analyzer` tool to analyze the plant image. "
        "Only return the disease name in short, e.g., 'Powdery Mildew'."
    ),
    tools=[crop_disease_tool],
    output_key="disease_name"
)


# -----------------------------------
# 3. Agent 2: Remedies Finder Agent
# -----------------------------------
remedies_agent = LlmAgent(
    name="crop_remedies_agent",
    model="gemini-2.0-flash",
    description="Finds remedies for the detected crop disease.",
    instructions=(
        "You are an agricultural assistant. The user has a plant suffering from {disease_name}. "
        "Use Google Search to find **3 effective remedies** for this disease. "
        "Present them as a numbered list."
    ),
    tools=[google_search],
    output_key="remedies"
)


# -----------------------------------
# 4. Main Sequential Agent
# -----------------------------------
main_agent = SequentialAgent(
    name="final_crop_disease_assistant",
    sub_agents=[disease_agent, remedies_agent],
    description=(
        "This assistant takes a plant image, detects the disease, "
        "and then suggests effective remedies."
    )
)


# -----------------------------------
# 5. RUN THE AGENT
# -----------------------------------
if __name__ == "__main__":
    user_image_path = r"E:\Project_kisan\Agents\backend\agents\crop_disease_agent\plant.jpg"  # ✅ Change this

    # ADK Runner (pseudo-call)
    print("Analyzing disease...")
    response = main_agent.run({"image_path": user_image_path})

    print("\n✅ Final Output:")
    print(f"🌱 Disease Detected: {response.get('disease_name')}")
    print(f"💊 Remedies:\n{response.get('remedies')}")
