from pydantic import BaseModel, EmailStr, Field


class CreateUserRequestSchema(BaseModel):
    username: str = Field(..., description="usernane")
    password1: str = Field(..., description="Password", min_length=6)
    password2: str = Field(..., description="Password confirmaiton", min_length=6)
    email: EmailStr = Field(..., description="Email field")


class UserCreateResponceSchema(BaseModel):
    id: int = Field(..., description="Id")
    username: str = Field(..., description="usernane")
    email: EmailStr = Field(..., description="Email field")
    password: str = Field(..., description="Password")

    class Config:
        orm_mode = True


class RetriveUserResponseSchema(BaseModel):
    id: int = Field(..., description="Id")
    role: int = Field(default=2, description="Role")
    username: str = Field(..., description="usernane")
    email: EmailStr = Field(..., description="Email field")

    class Config:
        orm_mode = True
