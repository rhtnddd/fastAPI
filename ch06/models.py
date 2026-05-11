from pydantic import BaseModel, Field

class SnackCreate(BaseModel):
    name: str = Field(..., min_length=2)
    cost: int = Field(..., gt=0)
    stock: int = Field(..., gt=0)

class SnackResponse(BaseModel):
    name: str
    selling_price: int