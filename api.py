from fastapi import FastAPI, UploadFile
from fastapi.responses import RedirectResponse
from google.cloud import storage


app = FastAPI()
BUCKET_NAME = 'auto-srt-new-file-received'

ONE_MG = 1024 * 1024
CHUNK_SIZE = 30 * ONE_MG

@app.get("/")
async def redirect_typer():
    return RedirectResponse("/docs")

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):

    async def upload_blob(bucket_name, file_to_upload:UploadFile):
        """Uploads a file to the bucket."""
        try:
            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)

            blob = bucket.blob(blob_name=file_to_upload.filename, chunk_size=CHUNK_SIZE)
            

            with file_to_upload.file as file_obj:
                blob.upload_from_file(size=file_to_upload.size, content_type=file_to_upload.content_type, file_obj=file_obj)

            return(
                f"File {file_to_upload.filename} uploaded to {bucket_name}."
            )
        except Exception as e:
            return f"Error uploading file: {str(e)}"
        
    res = await upload_blob(BUCKET_NAME,file)

    return res

