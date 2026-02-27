from pydantic import BaseModel
from typing import List


class NewsResponse(BaseModel):
    headlines: List[str]


