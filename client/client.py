import random
from minio import Minio
import io
import os

# MinIO client setup
minio_client = Minio(
    "localhost:9000",
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=False
)

# Create lyrics bucket
bucket_name = "lyrics-bucket"
if not minio_client.bucket_exists(bucket_name):
    minio_client.make_bucket(bucket_name)

# Lyrics components
subjects = ["I", "You", "We", "They", "The stars", "My heart", "Your eyes", "The night"]
verbs = ["dance", "shine", "dream", "fly", "run", "sing", "love", "remember"]
objects = ["in the rain", "through the night", "like diamonds", "in December", "forever", "in New York"]
emotions = ["with joy", "with passion", "endlessly", "fearlessly", "magically", "perfectly"]

def generate_lyrics():
    verses = []
    for _ in range(4):  # Generate 4 verses
        verse = []
        for _ in range(4):  # 4 lines per verse
            line = f"{random.choice(subjects)} {random.choice(verbs)} {random.choice(objects)} {random.choice(emotions)}"
            verse.append(line)
        verses.append("\n".join(verse))
    
    return "\n\n".join(verses)

# Generate and upload 10 song lyrics
for i in range(10):
    lyrics = generate_lyrics()
    lyrics_bytes = lyrics.encode('utf-8')
    lyrics_data = io.BytesIO(lyrics_bytes)
    
    # Upload to MinIO
    object_name = f"song_{i+1}.txt"
    minio_client.put_object(
        bucket_name,
        object_name,
        lyrics_data,
        length=len(lyrics_bytes),
        content_type="text/plain"
    )
    
    # Create images bucket
    images_bucket = "images-bucket"
    if not minio_client.bucket_exists(images_bucket):
        minio_client.make_bucket(images_bucket)
    
    # Read and upload Taylor Swift image
    with open("taylor_swift.jpg", "rb") as file:
        file_data = file.read()
        file_stream = io.BytesIO(file_data)
        
        # Upload to MinIO
        minio_client.put_object(
            images_bucket,
            f"taylor_swift_{i+1}.jpg",
            file_stream,
            length=len(file_data),
            content_type="image/jpeg"
        )
        print("Uploaded Taylor Swift image to MinIO")
    
    
    print(f"Generated and uploaded {object_name}")
