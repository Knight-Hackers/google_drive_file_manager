# main.py

# imports
from fastapi import FastAPI
from routers import files, user
from fastapi.middleware.cors import CORSMiddleware

# create FastAPI instance
app = FastAPI(
    title="Drive Organizer API",
    version="1.0.0",
    description="Backend for analyzing and categorizing Google Drive documents."
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Frontend URLs allowed to talk to backend
    allow_credentials=True,
    allow_methods=["*"],    # Allow all HTTP methods
    allow_headers=["*"],    # Allow all headers (including Authorization)
)

@app.get("/")
def read_root():
    return {"message": "FastAPI is running."}

# register routers with app
app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(files.router, prefix="/files", tags=["Files"])