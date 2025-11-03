from fastapi import FastAPI, HTTPException
from app.models import User, UserCreate
from app.external_api import ExternalAPI

app = FastAPI(title="User API", version="1.0.0")
external_api = ExternalAPI()


@app.get("/")
async def root():
    return {"message": "User API is running"}


@app.get("/users", response_model=list[User])
async def get_all_users():
    """Get all users from external API"""
    try:
        return await external_api.get_all_users()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users/{user_id}", response_model=User)
async def get_user_by_id(user_id: int):
    """Get user by ID from external API"""
    try:
        user = await external_api.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/users", response_model=User)
async def create_user(user: UserCreate):
    """Create a new user"""
    try:
        return await external_api.create_user(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
