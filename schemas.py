from pydantic import BaseModel
class UserBase(BaseModel):
    email:str

class User(UserBase):
    id:int
    username:str
    role:str

    class Config:
        orm_mode=True    