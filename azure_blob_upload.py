import os, uuid, sys

from pathlib import Path
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient, BlobBlock

BASE_DIR = Path.cwd()
VENV_PATH = BASE_DIR / ".env"

load_dotenv(VENV_PATH)

AZURE_ACCOUNT_NAME = os.getenv("AZURE_ACCOUNT_NAME")
AZURE_ACCOUNT_KEY = os.getenv("AZURE_ACCOUNT_KEY")


MODOS = [
    'help', '-h',
    'list', '-l',
    'upload', '-u',
    'download', '-d',
]


def main():
    
    if sys.argv[1] not in MODOS:
        print("Modo incorreto. Usar -h para mais informações")
        return
    
    if sys.argc != 3:
        print("Forma incorreta. Usar -h para mais informações")
        return
    
    
    raise NotImplementedError



def novo_cliente_blob(container_nome, blob_name):
    blob_service_client = BlobServiceClient(account_url=f"https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/",
                                            credential=AZURE_ACCOUNT_KEY)

    blob_client = blob_service_client.get_blob_client(container=container_nome, blob=blob_name)
    
    return blob_client



def upload_arquivo_em_blocos(file_path: str, file_name: str, block_size: int):

    extensao = Path(file_path).suffix
    file_name += extensao    
    
    blob_client = novo_cliente_blob(file_name)

    with open(file=file_path, mode="rb") as file_stream:
        block_id_list = []

        while True:
            buffer = file_stream.read(block_size)
            if not buffer:
                break

            block_id = uuid.uuid4().hex
            block_id_list.append(BlobBlock(block_id=block_id))

            blob_client.stage_block(block_id=block_id, data=buffer, length=len(buffer))
            

        blob_client.commit_block_list(block_id_list)




def upload_em_blocos(file_handler, blob_name: str, block_size: int):
    
    blob_client = novo_cliente_blob(blob_name)

    with file_handler.file as file_stream:
        block_id_list = []

        while True:
            buffer = file_stream.read(block_size)
            if not buffer:
                break

            block_id = uuid.uuid4().hex
            block_id_list.append(BlobBlock(block_id=block_id))

            blob_client.stage_block(block_id=block_id, data=buffer, length=len(buffer))
            

        blob_client.commit_block_list(block_id_list)
    
    return blob_client.url




def download_blob(blob_name):
    blob_client = novo_cliente_blob(blob_name)
    if not blob_client.exists():
        raise NameError("Arquivo inexistente")
    
    blob_content = blob_client.download_blob()
    return blob_content




def dowload_stream_blob(blob_name):
    blob_client = novo_cliente_blob(blob_name)
    if not blob_client.exists():
        raise NameError("Arquivo inexistente")
    
    stream = blob_client.download_blob()
    for chunk in stream.chunks():
        yield chunk



if __name__ == "__main__":
    main()