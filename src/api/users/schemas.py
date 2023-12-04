from pydantic import UUID4, BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = None
    password: str


class CreateUser(UserBase):
    pass


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    is_admin: bool = False


class UserToken(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = None
