from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    department: str
    position: str
    joining_date: str
    salary: float
    status: str
    address: str

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    joining_date: Optional[str] = None
    salary: Optional[float] = None
    status: Optional[str] = None
    address: Optional[str] = None

class DocumentOut(BaseModel):
    id: int
    employee_id: int
    file_name: str
    file_path: str
    file_type: str
    uploaded_at: datetime

    class Config:
        from_attributes = True

class EmployeeOut(EmployeeBase):
    id: int
    employee_code: str
    created_at: datetime
    updated_at: datetime
    documents: List[DocumentOut] = []

    class Config:
        from_attributes = True
