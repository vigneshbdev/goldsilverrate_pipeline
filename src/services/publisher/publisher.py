from abc import ABC, abstractmethod

from src.models.post_data import PostData
from src.models.publisher_info import PublisherInfo


class Publisher(ABC):

    @abstractmethod
    def publish(
        self,
        post_data: PostData,
    ) -> PublisherInfo:
        pass