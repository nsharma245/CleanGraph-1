from models.utils import PyObjectId
from pydantic import BaseModel

class CreateUnitDetail(BaseModel):
    name: str
