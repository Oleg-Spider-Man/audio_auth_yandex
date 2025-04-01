import os
from typing import List
from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.params import File, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from my_app import schemas
from my_app.auth_.verification_token import get_current_user
from my_app.dependencies import get_async_session
from my_app.models import AudioFile
from my_app.operations.crud import get_audio_user


router = APIRouter(
    prefix="/audio",
    tags=["audio"]
)


@router.post("/upload-audio", response_model=schemas.AudioFileResponse)
async def upload_audio(
    file: UploadFile = File(...),
    filename: str = Form(...),
    email: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    # Проверка типа файла
    if file.filename.split(".")[-1].lower() not in ["mp3", "wav", "ogg"]:
        return JSONResponse({"error": "Неподдерживаемый формат файла"}, status_code=400)

    # Сохранение файла локально
    upload_dir = "audio_uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    file_extension = file.filename.split(".")[-1].lower()
    new_filename = f"{filename}.{file_extension}"

    file_path = os.path.join(upload_dir, new_filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # Добавление записи в базу данных
    audio_file = AudioFile(user_email=email, filename=new_filename, path=file_path)
    db.add(audio_file)
    await db.commit()

    return {"filename": filename, "path": file_path}


@router.get("/user/audio-files", response_model=List[schemas.AudioFileResponse])
async def get_audio_files(user_email: str = Depends(get_current_user), db: AsyncSession = Depends(get_async_session)):
    try:
        audio_files = await get_audio_user(user_email, db)
        return [{"filename": file.filename, "path": file.path} for file in audio_files]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
