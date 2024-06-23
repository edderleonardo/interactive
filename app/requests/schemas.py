from pydantic import BaseModel
from pydantic.fields import Field
from typing import Optional


class GrimorioSchema(BaseModel):
    name: str


class RequestBase(BaseModel):
    name: str = Field(..., title="Name", description="Name of the person", min_length=1)
    last_name: str = Field(..., title="Last Name", description="Last name of the person", min_length=1)
    identification: str = Field(..., title="Identification", description="Identification of the person")
    age: int = Field(..., title="Age", description="Age of the person", ge=1, le=99)
    affinity: str = Field(..., title="Affinity", description="Affinity of the person", min_length=1)


class RequestCreate(RequestBase):
    class Config:
        json_schema_extra = {
            "example": {
                "name": "John",
                "last_name": "Doe",
                "identification": "123456789",
                "age": 25,
                "affinity": "Fuego"
            }
        }


class RequestUpdate(BaseModel):
    name: Optional[str] = Field(None, title="Name", description="Name of the person", min_length=1)
    last_name: Optional[str] = Field(None, title="Last Name", description="Last name of the person", min_length=1)
    identification: Optional[str] = Field(None, title="Identification", description="Identification of the person")
    age: Optional[int] = Field(None, title="Age", description="Age of the person", ge=1, le=99)
    affinity: Optional[str] = Field(None, title="Affinity", description="Affinity of the person", min_length=1)


class RequestUpdateStatus(BaseModel):
    status: str = Field(..., title="Status", description="Status of the request", min_length=1, max_length=50)
