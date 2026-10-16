# check_setup.py
import os
from pathlib import Path
from dotenv import load_dotenv

def verify_environment() -> dict:
    load_dotenv()
    armoriq_key = os.getenv("ARMORIQ_API_KEY", "")
    gemini_key = os.getenv("GEMINI_API_KEY", "")
    sandbox_ok = Path("./sandbox_repo").exists()
    yaml_ok = Path("./armoriq.yaml").exists()

    return {
        "armoriq_key_configured": bool(armoriq_key and "replace" not in armoriq_key),
        "gemini_key_configured": bool(gemini_key and "replace" not in gemini_key),
        "sandbox_initialized": sandbox_ok,
        "armoriq_yaml_present": yaml_ok,
        "agent_id": os.getenv("ARMORIQ_AGENT_ID", "hydra-dev-agent"),
    }