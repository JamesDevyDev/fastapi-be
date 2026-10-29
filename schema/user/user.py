from pydantic import BaseModel, Field

class UserRegister(BaseModel):
    username: str = Field()
    password: str = Field()

class UserLogin(BaseModel):
    username: str =Field()
    password: str = Field()

class UserResponse(BaseModel):
    id: int
    username: str