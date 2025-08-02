from pydantic import BaseModel
from typing import List, Dict, Any



class InferenceInput(BaseModel):
    instances: List[Dict[str, Any]]