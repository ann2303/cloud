from minio import Minio
import time
from pathlib import Path
import os

def main():
    # Initialize MinIO client
    minio_client = Minio(
        "localhost:9000",
        access_key=os.getenv("MINIO_ACCESS_KEY"),
        secret_key=os.getenv("MINIO_SECRET_KEY"),
        secure=False
    )

    # Ensure bucket exists
    bucket_name = "images"
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)

    counter = 0
    image_path = Path(__file__).parent / "image.jpg"

    while True:
        try:
            # Generate unique filename with counter
            filename = f"image_{counter}.jpg"
            
            # Upload file to MinIO
            minio_client.fput_object(
                bucket_name,
                filename,
                image_path,
                content_type="image/jpeg"
            )
            print(f"Uploaded {filename}")
            
            counter += 1
            time.sleep(1)  # Wait 1 second between uploads
            
        except Exception as e:
            print(f"Upload error: {e}")
            break  # Exit loop on upload error
        
if __name__ == "__main__":
    main()
