from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from utility.password import hash_password, verify_password
from utility.auth import create_access_token, get_current_user_id

from utility.dependencies import get_db

from schema.user.user import UserRegister, UserLogin

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    
    username = user.username.strip()
    password = user.password
    
    if not username.strip() or not password:
        raise HTTPException(
            status_code=400,
            detail="Username and password are required.",
        )
    
    if len(username) < 5 or len(username) > 30:
        raise HTTPException(
            status_code=400,
            detail="username should be 5 to 30 letters long."
        )
    
    if len(password) < 5 or len(password) > 30:
        raise HTTPException(
            status_code=400,
            detail="password should be 5 to 30 letters long."
        )
        
    is_user_exist = db.execute(text("""
                                    SELECT * from users
                                    WHERE username = :username
                                    """),{"username" : username})
    
    if is_user_exist.first():
        raise HTTPException(
            status_code=400,
            detail="user already exist."
        )
    
    hashed_pw = hash_password(password)
    
    db.execute(text("""
                        INSERT INTO users(username,password)
                        VALUES(:username, :password)
                    """),{"username": username, "password" : hashed_pw})
    
    db.commit()
    
    return {
        "sucess": "user has been created",
        "user" : username
    }
    
@router.post('/login')
def login(user: UserLogin, db: Session = Depends(get_db)):
    
    username = user.username.strip()
    password = user.password
    
    if not username.strip() or not password:
            raise HTTPException(
                status_code=400,
                detail="Username and password are required.",
            )
    
    if len(username) < 5 or len(username) > 30:
            raise HTTPException(
                status_code=400,
                detail="username should be 5 to 30 letters long."
            )
        
    if len(password) < 5 or len(password) > 30:
            raise HTTPException(
                status_code=400,
                detail="password should be 5 to 30 letters long."
            )
    
    result = db.execute(text("""
                                    SELECT * from users
                                    WHERE username = :username
                                    """),{"username" : username})
    
    existing_user = result.mappings().first()
    
    is_allowed = verify_password(password, existing_user.password)
    
    if not is_allowed:
        raise HTTPException(
            status_code=400,
            detail="username or password is incorrect."
        )
    
    token = create_access_token(existing_user.id)
    
    return {
        "success" : True,
        "token" : token
    }
    
@router.post('/validated-token/{token}')
def validate(token:str, db: Session = Depends(get_db)):
    is_allowed = get_current_user_id(token)
    
    logged_in = db.execute(text("""
                                SELECT * FROM users
                                WHERE id = id
                                """),{"id": is_allowed})
    
    return logged_in.mappings().first()