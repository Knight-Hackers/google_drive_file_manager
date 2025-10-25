# main.py

# imports
from fastapi import FastAPI
from routers import files, user

# create FastAPI instance
app = FastAPI(
    title="Drive Organizer API",
    version="1.0.0",
    description="Backend for analyzing and categorizing Google Drive documents."
)

# register routers with app
app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(files.router, prefix="/files", tags=["Files"])