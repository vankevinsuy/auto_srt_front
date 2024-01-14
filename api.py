from fastapi import FastAPI, UploadFile
from fastapi.responses import RedirectResponse
from google.cloud import storage


app = FastAPI()
BUCKET_NAME = 'auto-srt-new-file-received'


@app.get("/")
async def redirect_typer():
    return RedirectResponse("/docs")

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):

    async def upload_blob(bucket_name, file_to_upload:UploadFile):
        """Uploads a file to the bucket."""

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)

        data_as_bytes = await(file_to_upload.read())
        blob = bucket.blob(file_to_upload.filename)
        blob.upload_from_string(data_as_bytes)

        return(
            f"File {file_to_upload.filename} uploaded to {bucket_name}."
        )

    res = await upload_blob(BUCKET_NAME,file)

    return res

