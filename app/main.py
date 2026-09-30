from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

from app.database import engine, Base
from app.routers import pages
from app.seed import seed_database

app = FastAPI(title="WorkForce HR - Employee Management System")

# Create database tables if they do not exist, or auto seed if db file missing
db_path = "workforce_hr.db"
if not os.path.exists(db_path):
    print("Database not found. Initializing and seeding database...")
    seed_database()
else:
    Base.metadata.create_all(bind=engine)

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Include Routers
app.include_router(pages.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
