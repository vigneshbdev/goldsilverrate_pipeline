from src.agents.gold_rate_agent import GoldRateAgent
from src.agents.caption_agent import CaptionAgent
from src.agents.review_agent import ReviewAgent

from src.services.renderer.render_image import render_gold_silver_post
from src.services.uploader.image_uploader import (
    upload_image,
    prepare_instagram_image,
)
from src.services.publisher.publisher_factory import get_publisher

from src.tools.post_data_parser import PostDataParser

from src.models.gold_silver_rate import GoldSilverRate


def log(step: str, message: str):
    print(f"[{step:<12}] {message}")


def main():

    print()
    print("=" * 70)
    print("        🪙 GOLD & SILVER RATE AGENT PIPELINE")
    print("=" * 70)
    print()

    log("PIPELINE", "Starting automated gold & silver rate workflow")

    # ---------------------------------------------------------
    # 1. Initialize post data
    # ---------------------------------------------------------

    log("INIT", "Initializing post data")

    post_data = PostDataParser()

    # ---------------------------------------------------------
    # 2. Gold Rate Agent
    # ---------------------------------------------------------

    log("AGENT", "Starting Gold Rate Agent")
    log("AGENT", "Requesting today's Chennai gold & silver rates")

    rate_data = GoldRateAgent().run(
        "Give me todays gold rate"
    )

    if not isinstance(rate_data, GoldSilverRate):
        raise TypeError(
            f"Expected GoldSilverRate, got {type(rate_data).__name__}"
        )

    log("TOOL", "Gold rate tool executed successfully")

    log(
        "RATE",
        f"22K Gold: ₹{rate_data.gold22KRate.rate}/g "
        f"({rate_data.gold22KRate.diff:+g})"
    )

    log(
        "RATE",
        f"24K Gold: ₹{rate_data.gold24KRate.rate}/g "
        f"({rate_data.gold24KRate.diff:+g})"
    )

    log(
        "RATE",
        f"Silver: ₹{rate_data.silverRate.rate}/g "
        f"({rate_data.silverRate.diff:+g})"
    )

    post_data.update_gold_rate(rate_data)

    # ---------------------------------------------------------
    # 3. Caption Agent
    # ---------------------------------------------------------

    log("AGENT", "Starting Caption Agent")

    caption_data = CaptionAgent().run(
        rate_context=rate_data
    )

    post_data.update_captions(caption_data)

    log("CAPTION", "Instagram caption generated successfully")

    # ---------------------------------------------------------
    # 4. Review Agent
    # ---------------------------------------------------------

    log("AGENT", "Starting Review Agent")

    review_data = ReviewAgent().run(
        post_data=post_data.post_data
    )

    post_data.update_decision(review_data)

    log(
        "REVIEW",
        f"Decision: {'APPROVED' if post_data.post_data.decision else 'REJECTED'}"
    )

    # ---------------------------------------------------------
    # 5. Publish only when approved
    # ---------------------------------------------------------

    if not post_data.post_data.decision:

        log(
            "PIPELINE",
            "Post rejected by Review Agent. Publishing stopped."
        )

        print()
        print("=" * 70)
        print("        ❌ PIPELINE COMPLETED — POST NOT PUBLISHED")
        print("=" * 70)
        print()

        return

    # ---------------------------------------------------------
    # 6. Render image
    # ---------------------------------------------------------

    log("RENDER", "Rendering Instagram image")

    output_path = "src/assets/output/rendered_image.png"
    template_path = "src/assets/templates/gold_silver_rate_template.png"

    render_gold_silver_post(
        post_data=post_data.post_data,
        output_path=output_path,
        template_path=template_path,
    )

    log("RENDER", f"Image generated: {output_path}")

    # ---------------------------------------------------------
    # 7. Prepare image
    # ---------------------------------------------------------

    log("UPLOAD", "Preparing image for Instagram")

    upload_image_uri = prepare_instagram_image(
        output_path
    )

    # ---------------------------------------------------------
    # 8. Upload image
    # ---------------------------------------------------------

    log("UPLOAD", "Uploading image to Cloudinary")

    image_uri = upload_image(
        upload_image_uri
    )

    post_data.update_imageuri(
        imageuri=image_uri
    )

    log("UPLOAD", "Image uploaded successfully")

    # ---------------------------------------------------------
    # 9. Publish to Instagram
    # ---------------------------------------------------------

    log("PUBLISH", "Initializing Instagram publisher")

    publisher = get_publisher()

    log("PUBLISH", "Publishing post to Instagram")

    publisher_info = publisher.publish(
        post_data.post_data
    )

    log(
        "PUBLISH",
        f"Status: {publisher_info.status}"
    )

    # ---------------------------------------------------------
    # 10. Completed
    # ---------------------------------------------------------

    print()
    print("=" * 70)
    print("        ✅ GOLD & SILVER POST PIPELINE COMPLETED")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()