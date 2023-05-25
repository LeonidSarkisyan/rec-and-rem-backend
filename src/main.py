from fastapi import FastAPI

app = FastAPI(title='Rec & Rem Backend')


@app.get('/')
def home():
    return {'status': 'Ok'}
