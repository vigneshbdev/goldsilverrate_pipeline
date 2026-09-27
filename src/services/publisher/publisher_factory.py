import os

from src.services.publisher.publisher import Publisher
from src.services.publisher.providers.mock_instagram_publisher import MockInstagramPublisher
from src.services.publisher.providers.InstagramPublisher import InstagramPublisher


def get_publisher() -> Publisher:

    publisher_type = os.getenv(
        "PUBLISHER_TYPE",
        "mock"
    ).lower()

    if publisher_type == "mock":
        return MockInstagramPublisher()

    if publisher_type == "instagram":
        return InstagramPublisher()

    raise ValueError(
        f"Unsupported publisher type: {publisher_type}"
    )