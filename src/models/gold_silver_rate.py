from pydantic import BaseModel, Field
from datetime import date

class RateDiff(BaseModel):
    rate: float = Field(gt=0)
    diff: float

class GoldSilverRate(BaseModel):
    date: date
    gold22KRate: RateDiff
    gold24KRate: RateDiff
    silverRate: RateDiff