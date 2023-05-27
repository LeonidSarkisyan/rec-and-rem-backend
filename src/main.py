from fastapi import FastAPI

from auth.routers.auth import router as auth_router
from auth.routers.user import router as user_router


app = FastAPI(title='Rec & Rem Backend')

app.include_router(auth_router)
app.include_router(user_router)


@app.get('/')
def home():
    return {'status': 'Ok'}
