import os

from pathlib import Path
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

BASE_DIR = Path(__file__).resolve()
VENV_PATH = BASE_DIR / ".env"

load_dotenv(VENV_PATH)

AZURE_ACCOUNT_NAME=os.getenv("AZURE_ACCOUNT_NAME")
AZURE_ACCOUNT_KEY=os.getenv("AZURE_ACCOUNT_KEY")




def upload_basico(file_path, container_name):
    blob_service_client = BlobServiceClient(account_url=f"https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/",
                                            credential=AZURE_ACCOUNT_KEY)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_path)

    with open(file_path, "rb") as data:
        blob_client.upload_blob(data)
