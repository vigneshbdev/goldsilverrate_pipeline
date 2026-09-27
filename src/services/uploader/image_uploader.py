import os
from pathlib import Path

from PIL import Image
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()


def prepare_instagram_image(image_path: str) -> str:
    source = Path(image_path)

    if not source.exists():
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    output = source.parent / f"{source.stem}_instagram.jpg"

    with Image.open(source) as image:

        # Instagram-friendly 4:5 portrait dimensions
        image = image.convert("RGB")
        image = image.resize((1080, 1350), Image.Resampling.LANCZOS)

        image.save(
            output,
            format="JPEG",
            quality=90,
            optimize=True,
            progressive=False,
        )

    return str(output)


def upload_image(image_path: str) -> str:

    instagram_image = prepare_instagram_image(image_path)

    image = Path(instagram_image)

    print("\nINSTAGRAM IMAGE PREPARED")
    print(f"Path: {image}")
    print(f"Size: {image.stat().st_size / 1024:.2f} KB")

    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        secure=True,
    )

    upload_result = cloudinary.uploader.upload(
        str(image),
        folder="goldsilverratepipeline",
        resource_type="image",
    )

    secure_url = upload_result["secure_url"]

    print("\nCLOUDINARY UPLOAD SUCCESS")
    print("\nCLOUDINARY METADATA")
    print("format:", upload_result.get("format"))
    print("resource_type:", upload_result.get("resource_type"))
    print("type:", upload_result.get("type"))
    print("width:", upload_result.get("width"))
    print("height:", upload_result.get("height"))
    print("bytes:", upload_result.get("bytes"))
    print("content_type:", upload_result.get("resource_type"))
    print(f"Public URL: {secure_url}")

    return secure_url