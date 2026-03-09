import os
import json
import base64
from pathlib import Path
from dotenv import load_dotenv

load_dotenv("example.env")

XAI_API_KEY = os.getenv("XAI_API_KEY", "")


def encode_image_to_base64(image_path: str):
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def encode_video_to_base64(video_path: str):
    path = Path(video_path)
    if not path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")
    with open(video_path, "rb") as video_file:
        return base64.b64encode(video_file.read()).decode("utf-8")


def extract_usage(response):
    
    if not response.usage:
        return {}
    return {
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "reasoning_tokens": response.usage.reasoning_tokens,
        "total_tokens": response.usage.total_tokens,
    }

def load_history(session: str):
    path = Path("chats") / f"{session}.json"
    if path.exists():
        return json.loads(path.read_text())
    return []


def save_history(session: str, history: list):
    Path("chats").mkdir(exist_ok=True)
    (Path("chats") / f"{session}.json").write_text(json.dumps(history, indent=2, ensure_ascii=False))


def build_params(**kwargs):
    result = {}
    for key, value in kwargs.items():
        if value:
            result[key] = value
    return result