from pathlib import Path
from uuid import uuid4

from src.models.post_data import PostData
from src.models.publisher_info import PublisherInfo

from src.services.publisher.publisher import Publisher


class MockInstagramPublisher(Publisher):

    def publish(
        self,
        post_data: PostData
    ) -> PublisherInfo:

        print("\n" + "=" * 60)
        print("MOCK INSTAGRAM PUBLISHER")
        print("=" * 60)

        image = Path(post_data.imageURI)

        if not image.exists():
            raise FileNotFoundError(
                f"Instagram image not found: {post_data.imageURI}"
            )

        print("\nUploading image...")
        print(f"Image: {post_data.imageURI}")

        print("\nUploading caption...")
        print(post_data.captions)

        result = PublisherInfo(
            success=True,
            platform="instagram",
            mode="mock",
            post_id=f"MOCK_{uuid4().hex[:12]}",
            image=post_data.imageURI,
            caption=post_data.captions,
            status="PUBLISHED",
        )

        print("\nMOCK INSTAGRAM RESPONSE:")
        print(result)

        return result