# manager/tools/prompt_loader.py

import yaml
import os

def load_prompt(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
