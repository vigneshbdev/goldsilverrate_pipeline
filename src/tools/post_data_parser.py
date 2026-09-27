from src.models.post_data import PostData
from src.models.gold_silver_rate import GoldSilverRate
from datetime import date

class PostDataParser:

    def __init__(self) -> None:
        self.post_data = PostData(
            date=date.today(),
            gold22kDiff=0,
            gold22kRate=0,
            gold24kDiff=0,
            gold24kRate=0,
            silverDiff=0,
            silverRate=0,
            decision=False,
            captions="",
            reason="",
            imageURI=""
        )

    def update_gold_rate(self, rates: GoldSilverRate):
        self.post_data.gold22kDiff = rates.gold22KRate.diff
        self.post_data.gold22kRate = rates.gold22KRate.rate

        self.post_data.gold24kDiff = rates.gold24KRate.diff
        self.post_data.gold24kRate = rates.gold24KRate.rate

        self.post_data.silverDiff = rates.silverRate.diff
        self.post_data.silverRate = rates.silverRate.rate

    def update_captions(self, captions: str):
        self.post_data.captions = captions
    
    def update_decision(self, decision: str):
        self.post_data.decision = bool(decision)

    def update_imageuri(self, imageuri: str):
        self.post_data.imageURI = imageuri