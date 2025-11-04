from mem0 import Memory
import os

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


def get_mem0_client():
    config_file_path = os.getenv("CONFIG_FILE")
    if config_file_path == None or config_file_path == "":
        raise Exception(
            "Config file path is empty! please check environment variable CONFIG_FILE")

    return Memory.from_config_file(config_file_path)
