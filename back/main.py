from dotenv import load_dotenv

from services.auth import get_current_user_email
load_dotenv()

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import cards_router, collection_router, sets_router

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://tcgb-front-780761084412.europe-west9.run.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    cards_router,
    prefix='/api/cards',
    dependencies=[Depends(get_current_user_email)],
    tags=['Cards']
)

app.include_router(
    collection_router,
    prefix='/api/collection',
    dependencies=[Depends(get_current_user_email)],
    tags=['Collection']
)

app.include_router(
    sets_router,
    prefix='/api/sets',
    dependencies=[Depends(get_current_user_email)],
    tags=['Sets']
)
