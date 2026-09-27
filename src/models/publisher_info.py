from pydantic import BaseModel


class PublisherInfo(BaseModel):
    success: bool
    platform: str
    mode: str
    post_id: str
    image: str
    caption: str
    status: str