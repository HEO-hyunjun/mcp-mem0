import re
from dotenv import load_dotenv
from mem0 import Memory
import os
import yaml

load_dotenv()

# Custom instructions for memory processing
# These aren't being used right now but Mem0 does support adding custom prompting
# for handling memory retrieval and processing.
CUSTOM_INSTRUCTIONS = """
Extract the Following Information:  

- Key Information: Identify and save the most important details.
- Context: Capture the surrounding context to understand the memory's relevance.
- Connections: Note any relationships to other topics or memories.
- Importance: Highlight why this information might be valuable in the future.
- Source: Record where this information came from when applicable.
"""

def resolve_env_vars(obj):
    if isinstance(obj, dict):
        return {k: resolve_env_vars(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [resolve_env_vars(i) for i in obj]
    elif isinstance(obj, str):
        # Replace ${VAR} with actual env variable
        return re.sub(r"\$\{([^}^{]+)\}", lambda m: os.getenv(m.group(1), m.group(0)), obj)
    else:
        return obj

def get_mem0_client():
    # Load Mem0 client configuration from a YAML file
    config = {}
    
    with open("./mem0_config.yml") as f:
        config = yaml.safe_load(f)

    config = resolve_env_vars(config)

    return Memory.from_config(config)
