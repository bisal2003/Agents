import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

list_of_files = [
    # === Frontend (React Web) ===
    "frontend/src/components/AgentChatUI/__init__.py",
    "frontend/src/components/DiseaseScanner/__init__.py",
    "frontend/src/components/MarketDashboard/__init__.py",
    "frontend/src/components/SchemesAdvisory/__init__.py",
    "frontend/src/components/Shared/__init__.py",
    "frontend/src/pages/Home.js",
    "frontend/src/pages/CropHealth.js",
    "frontend/src/pages/MarketInsights.js",
    "frontend/src/pages/GovtSchemes.js",
    "frontend/src/utils/voice.js",
    "frontend/src/utils/api.js",
    "frontend/src/App.js",
    "frontend/public/.gitkeep",
    "frontend/package.json",

    # === Mobile App (React Native) ===
    "mobile-app/App.js",
    "mobile-app/package.json",
    "mobile-app/src/components/ChatUI.js",
    "mobile-app/src/components/CameraScanner.js",
    "mobile-app/src/components/VoiceAssistant.js",
    "mobile-app/src/screens/HomeScreen.js",
    "mobile-app/src/screens/CropHealthScreen.js",
    "mobile-app/src/screens/MarketInsightsScreen.js",
    "mobile-app/src/screens/GovtSchemesScreen.js",
    "mobile-app/src/utils/api.js",
    "mobile-app/src/utils/voice.js",
    "mobile-app/src/navigation/AppNavigator.js",

    # === Backend (FastAPI Microservices) ===
    "backend/main.py",
    "backend/agents/crop_disease_agent/service.py",
    "backend/agents/market_insights_agent/service.py",
    "backend/agents/govt_schemes_agent/service.py",
    "backend/agents/orchestrator/orchestrator_service.py",
    "backend/agents/orchestrator/pubsub.py",
    "backend/utils/firebase_cache.py",
    "backend/utils/stt_tts.py",
    "backend/requirements.txt",

    # === Data Pipeline ===
    "data-pipeline/crop_disease_training/train_gemini_vision.py",
    "data-pipeline/market_forecasting/train_bigquery_arima.sql",
    "data-pipeline/schemes_vectorization/embed_schemes_gemini.py",

    # === Infra & Docs ===
    "infra/docker/backend.Dockerfile",
    "infra/docker/frontend.Dockerfile",
    "infra/docker/cloudrun.yaml",
    "docs/hackathon_pitch.md",
    "README.md",
    ".env",
    ".gitignore"
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir:
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, 'w') as f:
            pass
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} already exists")
