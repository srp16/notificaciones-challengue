from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    email: str = Field(min_length=1, max_length=250)
    password: str = Field(min_length=1, max_length=50)
    
class UserRead(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    email: str = Field(min_length=1, max_length=250)
    
class LoginRead(BaseModel):
    email: str= Field(max_length=250)
    password: str = Field(min_length=1, max_length=50)
    
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"