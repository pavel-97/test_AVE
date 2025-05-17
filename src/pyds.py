from pydantic import BaseModel, Field


class SPhone(BaseModel):
    address: str
    phone: int = Field(ge=10 ** 10, lt=10 ** 11)
    