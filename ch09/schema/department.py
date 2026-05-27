from pydantic import BaseModel, ConfigDict

class DepartmentCreate(BaseModel):
    name: str
    personnel: int

class DepartmentResponse(DepartmentCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int