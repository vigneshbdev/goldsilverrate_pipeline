import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

from src.services.publisher.publisher import Publisher

from src.models.post_data import PostData
from src.models.publisher_info import PublisherInfo


load_dotenv()


GRAPH_API_URL = "https://graph.instagram.com"


class InstagramPublisher(Publisher):

    def __init__(self):
        self.access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
        self.instagram_account_id = os.getenv("INSTAGRAM_ACCOUNT_ID")

        if not self.access_token:
            raise ValueError(
                "INSTAGRAM_ACCESS_TOKEN is not configured"
            )

        if not self.instagram_account_id:
            raise ValueError(
                "INSTAGRAM_ACCOUNT_ID is not configured"
            )

    def publish(
        self,
        post_data: PostData
    ) -> PublisherInfo:

        print("\n[2/3] Creating Instagram media container...")

        container_id = self._create_media_container(
            image_url=post_data.imageURI,
            caption=post_data.captions,
        )

        print(f"Container ID: {container_id}")

        print("\n[3/3] Publishing Instagram post...")

        self._wait_for_container(container_id)

        media_id = self._publish_container(container_id)

        print("\nINSTAGRAM PUBLISH SUCCESS")
        print(f"Media ID: {media_id}")

        return PublisherInfo(
            success=True,
            platform="instagram",
            mode="real",
            post_id=media_id,
            image=post_data.imageURI,
            caption=post_data.captions,
            status="PUBLISHED",
        )

    def _create_media_container(
        self,
        image_url: str,
        caption: str,
    ) -> str:

        url = (
            f"{GRAPH_API_URL}/"
            f"{self.instagram_account_id}/media"
        )

        params = {
            "image_url": image_url,
            "caption": caption,
            "access_token": self.access_token,
        }

        response = requests.post(
            url,
            params=params,
            timeout=60,
        )

        self._raise_for_instagram_error(
            response,
            "creating media container",
        )

        data = response.json()

        container_id = data.get("id")

        if not container_id:
            raise RuntimeError(
                f"Instagram did not return container ID: {data}"
            )

        return container_id

    def _wait_for_container(
        self,
        container_id: str,
        max_attempts: int = 10,
        wait_seconds: int = 5,
    ):

        url = f"{GRAPH_API_URL}/{container_id}"

        for attempt in range(1, max_attempts + 1):

            params = {
                "fields": "status_code,status",
                "access_token": self.access_token,
            }

            response = requests.get(
                url,
                params=params,
                timeout=30,
            )

            self._raise_for_instagram_error(
                response,
                "checking container status",
            )

            data = response.json()

            status_code = data.get("status_code")
            status = data.get("status")

            print(
                f"Container status "
                f"[{attempt}/{max_attempts}]: "
                f"{status_code or status}"
            )

            if status_code == "FINISHED":
                return

            if status_code == "ERROR":
                raise RuntimeError(
                    f"Instagram media processing failed: {data}"
                )

            time.sleep(wait_seconds)

        raise TimeoutError(
            "Instagram media container did not finish "
            "processing within the expected time."
        )

    def _publish_container(
        self,
        container_id: str,
    ) -> str:

        url = (
            f"{GRAPH_API_URL}/"
            f"{self.instagram_account_id}/media_publish"
        )

        params = {
            "creation_id": container_id,
            "access_token": self.access_token,
        }

        response = requests.post(
            url,
            params=params,
            timeout=60,
        )

        self._raise_for_instagram_error(
            response,
            "publishing media container",
        )

        data = response.json()

        media_id = data.get("id")

        if not media_id:
            raise RuntimeError(
                f"Instagram did not return media ID: {data}"
            )

        return media_id

    @staticmethod
    def _raise_for_instagram_error(
        response: requests.Response,
        operation: str,
    ):

        if response.ok:
            return

        try:
            error_data = response.json()
        except ValueError:
            error_data = response.text

        raise RuntimeError(
            f"Instagram API error while {operation}.\n"
            f"HTTP {response.status_code}\n"
            f"Response: {error_data}"
        )