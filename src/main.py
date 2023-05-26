from fastapi import FastAPI

from auth.router import router as auth_router

app = FastAPI(title='Rec & Rem Backend')

app.include_router(auth_router)


@app.get('/')
def home():
    return {'status': 'Ok'}


# ЭТО ВЕРСИЯ ДЛЯ НОУТБУКА
