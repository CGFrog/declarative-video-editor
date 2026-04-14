import os
import tempfile
from uuid import uuid4

def generate_temp_path(suffix=".mp4")->str:
    temp_dir = tempfile.gettempdir()
    return os.path.join(temp_dir, f"{uuid4()}{suffix}")