from minio import Minio
import time
from pathlib import Path
import os
import sys
import logging
logging.basicConfig(handlers=[logging.StreamHandler(sys.stdout)], level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def send_loop(minio_client, bucket_name, image_path, left, right):
    counter = left
    for _ in range(left, right):
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
            logging.info(f"Uploaded {filename}")
            time.sleep(0.1)
            
            counter += 1
            
        except Exception as e:
            print(f"Upload error: {e}")
            sys.exit(0)  # Exit loop on upload error
        

def main():
    
    # Initialize MinIO client
    logging.info("Starting data transfer to MinIO...")
    minio_client = Minio(
        f"{os.getenv('MINIO_HOST')}:{os.getenv('MINIO_PORT')}",
        access_key=os.getenv("MINIO_ACCESS_KEY"),
        secret_key=os.getenv("MINIO_SECRET_KEY"),
        secure=False
    )

    # Ensure bucket exists
    bucket_name = "images"
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)

    image_path = Path(__file__).parent / "image.jpg"
    
    # Calculate image size
    image_size = os.path.getsize(image_path)
    logging.info(f"Image size: {image_size} bytes")
    
    storage_limited_count = int(float(os.getenv("STORAGE_SIZE").replace("M", "")) * 1024 * 1024) // image_size + 1
    quota_limited_count = int(float(os.getenv("QUOTA").replace("MB", "")) * 1024 * 1024) // image_size + 1
    
    logging.info(f"Storage limited count: {storage_limited_count}")
    logging.info(f"Quota limited count: {quota_limited_count}")
    
    right = quota_limited_count
    send_loop(minio_client, bucket_name, image_path, 0, right)
    

    logging.info("Quota limit reached. Waiting for 2 minutes...")
    time.sleep(120)
    
    try:
        # Generate unique filename with counter
        filename = f"image_{right}.jpg"
        
        # Upload file to MinIO
        minio_client.fput_object(
            bucket_name,
            filename,
            image_path,
            content_type="image/jpeg"
        )
        logging.info(f"Uploaded {filename}")
        time.sleep(0.5)
                
    except Exception as e:
        print(f"Upload error: {e}")
    
    
    
        
if __name__ == "__main__":
    main()
