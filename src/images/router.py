from fastapi import Depends, APIRouter, File, UploadFile

from src.images.service import ImageService

from src.auth.depends import get_current_user
from src.auth.models import User


router = APIRouter(prefix='/images', tags=['Images'])


@router.post('/')
def upload_image(file: UploadFile = File(), user: User = Depends(get_current_user)):
    key = ImageService.upload_image(file)
    return key


@router.get('/')
def download_image(key: str, user: User = Depends(get_current_user)):
    return ImageService.download_image(key)
