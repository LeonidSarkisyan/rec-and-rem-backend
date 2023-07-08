from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from src.auth.routers.auth import router as auth_router
from src.auth.routers.user import router as user_router
from src.profiles.router import router as profile_router
from src.workspace.router import router as workspace_router
from src.folder.router import router as folder_router
from src.folder.router import router_without_workspace_id as folder_router_without_workspace_id
from src.abstract.router import router as abstract_router
from src.abstract.router import router_without_folder_id as abstract_router_without_router_id

import boto3
from src.config import YandexS3Config


app = FastAPI(title='Rec & Rem Backend')


origins = ["http://localhost:3000", 'https://localhost:8080']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie"]
)


app.include_router(abstract_router)
app.include_router(abstract_router_without_router_id)
app.include_router(folder_router)
app.include_router(folder_router_without_workspace_id)
app.include_router(workspace_router)
app.include_router(profile_router)
app.include_router(user_router)
app.include_router(auth_router)


@app.get('/')
def home():
    return {'status': 'Ok'}


session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net',
    aws_access_key_id=YandexS3Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=YandexS3Config.AWS_SECRET_ACCESS_KEY,
    region_name='ru-central1'
)


@app.post('/file')
async def download_file(file: UploadFile = File()):
    s3.upload_fileobj(file.file, Bucket='rec-and-rem-test', Key=f'static/{file.filename}')
    return


@app.get('/file')
async def get_file():
    file = s3.get_object(Bucket='rec-and-rem-test', Key='static/globe.png')
    return StreamingResponse(file['Body'])
