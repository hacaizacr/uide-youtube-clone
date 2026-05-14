import os
import boto3
from fastapi import UploadFile
from dotenv import load_dotenv

load_dotenv()

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

def upload_file_to_s3(file: UploadFile, folder: str) -> str:
    file_path = f"{folder}/{file.filename}"
    try:
        s3_client.upload_fileobj(
            file.file,
            BUCKET_NAME,
            file_path,
            # Borramos la línea de ACL: "public-read"
            ExtraArgs={"ContentType": file.content_type} 
        )
        # Asegúrate de que el formato de la URL sea el correcto para tu región
        return f"https://{BUCKET_NAME}.s3.amazonaws.com/{file_path}"
    except Exception as e:
        raise Exception(f"Error al subir a S3: {str(e)}")