from pydantic import BaseModel, EmailStr,ConfigDict

class EmployeeCreate(BaseModel):
    employee_code : str
    name :str
    department : str
    email :EmailStr

class EmployeeResponse(BaseModel):
    id: int 
    employee_code:str
    name:str
    department:str
    email:EmailStr
    is_active:bool

    model_config=ConfigDict(from_attributes=True)
