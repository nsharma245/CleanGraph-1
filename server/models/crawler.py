from models.utils import PyObjectId
from pydantic import BaseModel

class CreateCrawler(BaseModel):
    name: str