from pydantic import BaseModel
from datetime import date

class PostData(BaseModel):
    date: date
    gold22kRate: float
    gold22kDiff: float
    gold24kRate: float
    gold24kDiff: float
    silverRate: float
    silverDiff: float
    captions: str
    imageURI: str
    decision: bool
    reason: str