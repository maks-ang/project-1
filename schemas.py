from pydantic import BaseModel, Field, EmailStr, ConfigDict


class CreateSchema(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    customer_name: str = Field(min_length=1, max_length=20)
    phone: str = Field(min_length=1, max_length=20)
    email: EmailStr | None = None
    order_details: str = Field(min_length=1)


class ReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    customer_name: str
    phone: str
    order_details: str

