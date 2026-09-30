from fastapi import APIRouter, Request, Depends, Form, File, UploadFile, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import Optional
import os
import re
import shutil
from datetime import datetime

from app.database import get_db
from app.models import User, Employee, Document
from app.auth import (
    get_current_user,
    verify_password,
    create_access_token,
    require_user,
    require_admin,
    require_admin_or_hr
)

router = APIRouter()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates"))

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

@router.get("/", response_class=HTMLResponse)
@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if user:
        if user.role in ["Admin", "HR Manager"]:
            return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
        else:
            return RedirectResponse(url="/profile", status_code=status.HTTP_302_FOUND)
    
    msg = request.query_params.get("msg")
    error = request.query_params.get("error")
    return templates.TemplateResponse(request=request, name="login.html", context={
        "success_msg": msg,
        "error_msg": error
    })

@router.post("/login", response_class=HTMLResponse)
def login_submit(
    request: Request,
    email: str = Form(""),
    password: str = Form(""),
    db: Session = Depends(get_db)
):
    email_clean = email.strip()
    password_clean = password.strip()

    # Validations
    if not email_clean:
        return templates.TemplateResponse(request=request, name="login.html", context={
            "error_msg": "Email is required",
            "email": email_clean
        }, status_code=400)
    
    if not password_clean:
        return templates.TemplateResponse(request=request, name="login.html", context={
            "error_msg": "Password is required",
            "email": email_clean
        }, status_code=400)

    if not re.match(EMAIL_REGEX, email_clean):
        return templates.TemplateResponse(request=request, name="login.html", context={
            "error_msg": "Invalid email format",
            "email": email_clean
        }, status_code=400)

    user = db.query(User).filter(User.email == email_clean).first()
    if not user or not verify_password(password_clean, user.password_hash):
        return templates.TemplateResponse(request=request, name="login.html", context={
            "error_msg": "Invalid email or password",
            "email": email_clean
        }, status_code=400)

    access_token = create_access_token({"sub": user.id, "role": user.role})
    
    redirect_url = "/dashboard" if user.role in ["Admin", "HR Manager"] else "/profile"
    response = RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=access_token, path="/", httponly=True)
    return response

@router.get("/logout")
def logout():
    response = RedirectResponse(url="/login?msg=Logged+out+successfully", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="access_token", path="/")
    return response

@router.get("/dashboard", response_class=HTMLResponse)
@router.get("/admin/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login?error=Please+login+to+access+dashboard", status_code=status.HTTP_302_FOUND)

    if user.role == "Employee":
        return RedirectResponse(url="/profile", status_code=status.HTTP_302_FOUND)

    total_employees = db.query(Employee).count()
    active_employees = db.query(Employee).filter(Employee.status == "Active").count()
    inactive_employees = db.query(Employee).filter(Employee.status == "Inactive").count()
    
    departments = db.query(Employee.department).distinct().all()
    total_departments = len(departments)

    recent_employees = db.query(Employee).order_by(Employee.id.desc()).limit(5).all()

    return templates.TemplateResponse(request=request, name="dashboard.html", context={
        "user": user,
        "total_employees": total_employees,
        "active_employees": active_employees,
        "inactive_employees": inactive_employees,
        "total_departments": total_departments,
        "recent_employees": recent_employees
    })

@router.get("/employees", response_class=HTMLResponse)
def employee_list(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user or user.role not in ["Admin", "HR Manager"]:
        return RedirectResponse(url="/profile", status_code=status.HTTP_302_FOUND)

    employees = db.query(Employee).order_by(Employee.id.asc()).all()
    success_msg = request.query_params.get("success")
    error_msg = request.query_params.get("error")

    return templates.TemplateResponse(request=request, name="employees.html", context={
        "user": user,
        "employees": employees,
        "success_msg": success_msg,
        "error_msg": error_msg
    })

@router.get("/employees/add", response_class=HTMLResponse)
def employee_add_form(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user or user.role not in ["Admin", "HR Manager"]:
        return RedirectResponse(url="/profile", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse(request=request, name="employee_form.html", context={
        "user": user,
        "is_edit": False
    })

@router.post("/employees/add", response_class=HTMLResponse)
def employee_add_submit(
    request: Request,
    first_name: str = Form(""),
    last_name: str = Form(""),
    email: str = Form(""),
    phone: str = Form(""),
    department: str = Form(""),
    position: str = Form(""),
    joining_date: str = Form(""),
    salary: str = Form(""),
    status_val: str = Form("Active", alias="status"),
    address: str = Form(""),
    db: Session = Depends(get_db)
):
    user = get_current_user(request, db)
    if not user or user.role not in ["Admin", "HR Manager"]:
        return RedirectResponse(url="/profile", status_code=status.HTTP_302_FOUND)

    form_data = {
        "first_name": first_name.strip(),
        "last_name": last_name.strip(),
        "email": email.strip(),
        "phone": phone.strip(),
        "department": department.strip(),
        "position": position.strip(),
        "joining_date": joining_date.strip(),
        "salary": salary.strip(),
        "status": status_val.strip(),
        "address": address.strip()
    }

    # 1. Required fields check
    for field, val in form_data.items():
        if not val:
            return templates.TemplateResponse(request=request, name="employee_form.html", context={
                "user": user,
                "is_edit": False,
                "error_msg": f"{field.replace('_', ' ').title()} is required",
                "form_data": form_data
            }, status_code=400)

    # 2. Email format validation
    if not re.match(EMAIL_REGEX, form_data["email"]):
        return templates.TemplateResponse(request=request, name="employee_form.html", context={
            "user": user,
            "is_edit": False,
            "error_msg": "Invalid email format",
            "form_data": form_data
        }, status_code=400)

    # 3. Phone format validation
    if not re.match(r"^\+?[\d\s-]{10,15}$", form_data["phone"]):
        return templates.TemplateResponse(request=request, name="employee_form.html", context={
            "user": user,
            "is_edit": False,
            "error_msg": "Invalid phone number format",
            "form_data": form_data
        }, status_code=400)

    # 4. Salary numeric validation
    try:
        salary_float = float(form_data["salary"])
        if salary_float <= 0:
            raise ValueError()
    except ValueError:
        return templates.TemplateResponse(request=request, name="employee_form.html", context={
            "user": user,
            "is_edit": False,
            "error_msg": "Salary must be a valid positive number",
            "form_data": form_data
        }, status_code=400)

    # 5. Date validation
    try:
        datetime.strptime(form_data["joining_date"], "%Y-%m-%d")
    except ValueError:
        return templates.TemplateResponse(request=request, name="employee_form.html", context={
            "user": user,
            "is_edit": False,
            "error_msg": "Invalid joining date format",
            "form_data": form_data
        }, status_code=400)

    # 6. Duplicate Email Check
    existing_emp = db.query(Employee).filter(Employee.email == form_data["email"]).first()
    existing_usr = db.query(User).filter(User.email == form_data["email"]).first()
    if existing_emp or existing_usr:
        return templates.TemplateResponse(request=request, name="employee_form.html", context={
            "user": user,
            "is_edit": False,
            "error_msg": "Employee with this email already exists",
            "form_data": form_data
        }, status_code=400)

    # Generate Employee Code guaranteed to be unique
    max_id = db.query(func.max(Employee.id)).scalar() or 0
    next_id = max_id + 1
    while db.query(Employee).filter(Employee.employee_code == f"EMP{next_id:03d}").first():
        next_id += 1
    employee_code = f"EMP{next_id:03d}"

    new_emp = Employee(
        employee_code=employee_code,
        first_name=form_data["first_name"],
        last_name=form_data["last_name"],
        email=form_data["email"],
        phone=form_data["phone"],
        department=form_data["department"],
        position=form_data["position"],
        joining_date=form_data["joining_date"],
        salary=salary_float,
        status=form_data["status"],
        address=form_data["address"]
    )
    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)

    return templates.TemplateResponse(request=request, name="employee_form.html", context={
        "user": user,
        "is_edit": False,
        "success_msg": "Employee created successfully"
    })

@router.get("/employees/{id}", response_class=HTMLResponse)
def employee_detail(id: int, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

    employee = db.query(Employee).filter(Employee.id == id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Employee role check: can only view own details
    if user.role == "Employee" and user.email != employee.email:
        return RedirectResponse(url="/profile", status_code=status.HTTP_302_FOUND)

    documents = db.query(Document).filter(Document.employee_id == employee.id).all()
    success_msg = request.query_params.get("success")
    error_msg = request.query_params.get("error")

    return templates.TemplateResponse(request=request, name="employee_detail.html", context={
        "user": user,
        "employee": employee,
        "documents": documents,
        "success_msg": success_msg,
        "error_msg": error_msg
    })

@router.get("/employees/{id}/edit", response_class=HTMLResponse)
def employee_edit_form(id: int, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user or user.role not in ["Admin", "HR Manager"]:
        return RedirectResponse(url="/profile", status_code=status.HTTP_302_FOUND)

    employee = db.query(Employee).filter(Employee.id == id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    return templates.TemplateResponse(request=request, name="employee_form.html", context={
        "user": user,
        "is_edit": True,
        "employee": employee
    })

@router.post("/employees/{id}/edit", response_class=HTMLResponse)
def employee_edit_submit(
    id: int,
    request: Request,
    first_name: str = Form(""),
    last_name: str = Form(""),
    email: str = Form(""),
    phone: str = Form(""),
    department: str = Form(""),
    position: str = Form(""),
    joining_date: str = Form(""),
    salary: str = Form(""),
    status_val: str = Form("Active", alias="status"),
    address: str = Form(""),
    db: Session = Depends(get_db)
):
    user = get_current_user(request, db)
    if not user or user.role not in ["Admin", "HR Manager"]:
        return RedirectResponse(url="/profile", status_code=status.HTTP_302_FOUND)

    employee = db.query(Employee).filter(Employee.id == id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    form_data = {
        "first_name": first_name.strip(),
        "last_name": last_name.strip(),
        "email": email.strip(),
        "phone": phone.strip(),
        "department": department.strip(),
        "position": position.strip(),
        "joining_date": joining_date.strip(),
        "salary": salary.strip(),
        "status": status_val.strip(),
        "address": address.strip()
    }

    # Validations
    if not re.match(EMAIL_REGEX, form_data["email"]):
        return templates.TemplateResponse(request=request, name="employee_form.html", context={
            "user": user,
            "is_edit": True,
            "employee": employee,
            "error_msg": "Invalid email format"
        }, status_code=400)

    if not re.match(r"^\+?[\d\s-]{10,15}$", form_data["phone"]):
        return templates.TemplateResponse(request=request, name="employee_form.html", context={
            "user": user,
            "is_edit": True,
            "employee": employee,
            "error_msg": "Invalid phone number format"
        }, status_code=400)

    try:
        salary_float = float(form_data["salary"])
    except ValueError:
        return templates.TemplateResponse(request=request, name="employee_form.html", context={
            "user": user,
            "is_edit": True,
            "employee": employee,
            "error_msg": "Salary must be a valid positive number"
        }, status_code=400)

    # Check duplicate email on another employee
    existing = db.query(Employee).filter(Employee.email == form_data["email"], Employee.id != id).first()
    if existing:
        return templates.TemplateResponse(request=request, name="employee_form.html", context={
            "user": user,
            "is_edit": True,
            "employee": employee,
            "error_msg": "Employee with this email already exists"
        }, status_code=400)

    employee.first_name = form_data["first_name"]
    employee.last_name = form_data["last_name"]
    employee.email = form_data["email"]
    employee.phone = form_data["phone"]
    employee.department = form_data["department"]
    employee.position = form_data["position"]
    employee.joining_date = form_data["joining_date"]
    employee.salary = salary_float
    employee.status = form_data["status"]
    employee.address = form_data["address"]
    employee.updated_at = datetime.utcnow()

    db.commit()

    return RedirectResponse(url=f"/employees/{id}?success=Employee+updated+successfully", status_code=status.HTTP_302_FOUND)

@router.post("/employees/{id}/delete")
def employee_delete(id: int, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

    if user.role != "Admin":
        return RedirectResponse(url="/employees?error=Only+Admin+can+delete+employees", status_code=status.HTTP_302_FOUND)

    employee = db.query(Employee).filter(Employee.id == id).first()
    if employee:
        db.delete(employee)
        db.commit()

    return RedirectResponse(url="/employees?success=Employee+deleted+successfully", status_code=status.HTTP_302_FOUND)

@router.post("/employees/{id}/upload")
def upload_document(
    id: int,
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(request, db)
    if not user or user.role not in ["Admin", "HR Manager"]:
        return RedirectResponse(url=f"/employees/{id}?error=Permission+denied", status_code=status.HTTP_302_FOUND)

    employee = db.query(Employee).filter(Employee.id == id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()
    
    if ext not in [".pdf", ".png", ".jpg", ".jpeg"]:
        return RedirectResponse(url=f"/employees/{id}?error=Invalid+file+format.+Allowed+formats:+PDF,+PNG,+JPG", status_code=status.HTTP_302_FOUND)

    file_type = "PDF" if ext == ".pdf" else ("PNG" if ext == ".png" else "JPG")
    
    uploads_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "uploads")
    os.makedirs(uploads_dir, exist_ok=True)
    
    saved_filename = f"{employee.employee_code}_{int(datetime.utcnow().timestamp())}_{filename}"
    file_path = os.path.join(uploads_dir, saved_filename)
    relative_path = f"static/uploads/{saved_filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_doc = Document(
        employee_id=employee.id,
        file_name=filename,
        file_path=relative_path,
        file_type=file_type
    )
    db.add(new_doc)
    db.commit()

    return RedirectResponse(url=f"/employees/{id}?success=Document+uploaded+successfully", status_code=status.HTTP_302_FOUND)

@router.get("/profile", response_class=HTMLResponse)
def profile_view(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

    employee = db.query(Employee).filter(Employee.email == user.email).first()
    msg = request.query_params.get("msg")
    error = request.query_params.get("error")

    return templates.TemplateResponse(request=request, name="profile.html", context={
        "user": user,
        "employee": employee,
        "success_msg": msg,
        "error_msg": error
    })

@router.post("/profile", response_class=HTMLResponse)
def profile_update(
    request: Request,
    phone: str = Form(""),
    address: str = Form(""),
    db: Session = Depends(get_db)
):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

    employee = db.query(Employee).filter(Employee.email == user.email).first()
    if employee:
        employee.phone = phone.strip()
        employee.address = address.strip()
        db.commit()

    return templates.TemplateResponse(request=request, name="profile.html", context={
        "user": user,
        "employee": employee,
        "success_msg": "Profile updated successfully"
    })

@router.get("/documents", response_class=HTMLResponse)
def documents_hub(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

    if user.role in ["Admin", "HR Manager"]:
        documents = db.query(Document).all()
    else:
        employee = db.query(Employee).filter(Employee.email == user.email).first()
        documents = db.query(Document).filter(Document.employee_id == employee.id).all() if employee else []

    return templates.TemplateResponse(request=request, name="documents.html", context={
        "user": user,
        "documents": documents
    })
