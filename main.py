from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from app.schemas import AppointmentForm, LoginRequest
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt
import datetime

from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import engine, SessionLocal
 
# สร้างตารางในฐานข้อมูล
models.Base.metadata.create_all(bind=engine)
 
app = FastAPI()

SECRET_KEY = "cn334_super_secret_key"
ALGORITHM = "HS256"

# ตั้งค่าให้อนุญาตการเชื่อมต่อจาก Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",  "https://cn334-frontend-chi.vercel.app/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Generator สำหรับจัดการ Database Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head><title>CN334 Web App</title></head>
        <body>
            <h1>Welcome to CN334 Backend Development</h1>
            <p>Supasin Boonprasert<p>
            <p>Port: 3340 is working!</p>
        </body>
    </html>
    """
@app.post("/")
async def create_data():
    return {"message": "Data received via POST method", "status": "success"}

@app.post("/appointments")
async def create_appointment(form_data: schemas.AppointmentForm,
db: Session = Depends(get_db)):
    print(f"Received data from Next.js: {form_data}")
    saved_data = crud.create_appointment(db=db, appointment=form_data)
    return {"status": "success", "message": "Appointment saved successfully",
    "data": saved_data}

@app.get("/appointments")
async def read_appointments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    appointments = crud.get_appointments(db, skip=skip, limit=limit)
    return {"status": "success", "data": appointments}

@app.post("/login")
async def login(request: LoginRequest):
    if request.username == "admin" and request.password == "password123":

        payload = {
            "sub": request.username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        
        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        
        return {
            "message": "Login successful",
            "access_token": access_token,
            "token_type": "bearer"
        }
    else:
        raise HTTPException(
            status_code=401, 
            detail="Invalid username or password"
        )

@app.post("/patients")
async def create_patient(record: schemas.PatientRecordCreate,
db: Session = Depends(get_db)):
    return crud.create_patient_record(db=db, record=record)

 

@app.get("/patients")
async def read_patients(skip: int = 0, limit: int = 100,
db: Session = Depends(get_db)):
    return crud.get_patient_records(db, skip=skip, limit=limit)

 

@app.put("/patients/{record_id}")
async def update_patient(record_id: int, record: schemas.PatientRecordCreate,
db: Session = Depends(get_db)):
    return crud.update_patient_record(db=db, record_id=record_id, record=record)

 

@app.delete("/patients/{record_id}")
async def delete_patient(record_id: int, db: Session = Depends(get_db)):
    crud.delete_patient_record(db=db, record_id=record_id)
    return {"message": "Patient record deleted successfully"}

@app.put("/appointments/{appointment_id}")
async def edit_appointment(appointment_id: int, form_data: schemas.AppointmentForm,
db: Session = Depends(get_db)):
    updated_data = crud.update_appointment(db=db, appointment_id=appointment_id,
    appointment=form_data)
    return {"status": "success", "data": updated_data}
 
@app.delete("/appointments/{appointment_id}")
async def remove_appointment(appointment_id: int, db: Session = Depends(get_db)):
    crud.delete_appointment(db=db, appointment_id=appointment_id)
    return {"status": "success", "message": "Appointment deleted successfully"}