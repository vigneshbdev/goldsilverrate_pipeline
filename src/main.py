from src.agents.gold_rate_agent import GoldRateAgent
from src.agents.caption_agent import CaptionAgent
from src.agents.review_agent import ReviewAgent

from src.services.renderer.render_image import render_gold_silver_post
from src.services.uploader.image_uploader import upload_image, prepare_instagram_image
from src.services.publisher.publisher_factory import get_publisher

from src.tools.post_data_parser import PostDataParser

from src.models.gold_silver_rate import GoldSilverRate

def main():
        post_data =PostDataParser()

        rate_data = GoldRateAgent().run(
                "Give me todays gold rate"
            )

        if not isinstance(rate_data,GoldSilverRate):
            raise TypeError(
                f"Expected GoldSilverRate, got {type(rate_data).__name__}"
            )
        
        post_data.update_gold_rate(rate_data)

        caption_data = CaptionAgent().run(rate_context=rate_data)
        post_data.update_captions(caption_data)

        review_data = ReviewAgent().run(post_data=post_data.post_data)
        post_data.update_decision(review_data)

        if post_data.post_data.decision:
            render_gold_silver_post(
                 post_data=post_data.post_data, 
                 output_path="src/assets/output/rendered_image.png", 
                 template_path="src/assets/templates/gold_silver_rate_template.png"
                )

            upload_image_uri = prepare_instagram_image("src/assets/output/rendered_image.png")
            image_uri = upload_image(upload_image_uri)

            post_data.update_imageuri(imageuri=image_uri)

            publisher = get_publisher()
            publisher_info = publisher.publish(post_data.post_data)

            print(publisher_info.status)

if __name__ == "__main__":
    main()