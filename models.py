from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, field_validator, Field, EmailStr, HttpUrl

class StatusType(str,Enum):
    DONE = "done"
    PENDING = "pending"

class MyBaseModel(BaseModel):
    id: int = Field(gt=1, le=100)
    
    @field_validator('id')
    def greater_than_zero(cls, v):
        if v <= 0:
            raise ValueError('must be greater than zero')
        return v
    


class Category(MyBaseModel):
    id: int
    name: str

class User(MyBaseModel):
    id: int 
    name: str = Field(min_length=5)
    surname: str
    email: EmailStr
    website: HttpUrl

class Task(MyBaseModel):
    id: int
    name: str
    description: Optional[str] = Field("No descripcion", min_length=5)
    status: StatusType
    category: Category
    user: User
    #tags: List[str] = []
    tags: set[str] = set()

    model_config = {
        "json_schema_extra":{
            "examples":[
                {
                    "id": 123,
                    "name": "Salvar a l mundo",
                    "description": "Hola mundo",
                    "status": StatusType.PENDING,
                    "tag": ["tag 1", "tag 2"],
                    "category": {
                        "id": 1234,
                        "name": "Cate 1"
                    },
                    "user": {
                        "name": "Andres",
                        "email": "admin@admin.com",
                        "surname": "Cruz",
                        "website": "https://desarrollolibre.net"

                    }
                }
            ]
        }
    }

    # @field_validator('name')
    # def name_alphanumeric_and_whitespace(cls, v):
    #     if v.isalnum():
    #         return v
    #     raise ValueError('must be a alphanumeric')
        