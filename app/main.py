from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.requests import models as requests_models
from app.requests.endpoints import router as user_router
from app.databases.database import engine


app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=['*'], allow_headers=['*']
)

requests_models.Base.metadata.create_all(bind=engine)

# Routes
app.include_router(user_router)


