from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import cards_router, collection_router

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    cards_router,
    prefix='/api/cards',
    tags=['Cards']
)

app.include_router(
    collection_router,
    prefix='/api/collection',
    tags=['Collection']
)
