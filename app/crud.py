from sqlalchemy.orm import Session
from app import models, schemas

def create_appointment(db: Session, appointment: schemas.AppointmentForm):
    db_appointment = models.Appointment(**appointment.model_dump())
    try:
        db.add(db_appointment)
        db.commit()
        db.refresh(db_appointment)
    except:
        db.rollback()
        raise
    return db_appointment


def get_appointments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Appointment).offset(skip).limit(limit).all()


def update_appointment(db: Session, appointment_id: int, appointment: schemas.AppointmentForm):
    db_appointment = (
        db.query(models.Appointment)
        .filter(models.Appointment.id == appointment_id)
        .first()
    )

    if not db_appointment:
        return None

    for key, value in appointment.model_dump(exclude_unset=True).items():
        setattr(db_appointment, key, value)

    try:
        db.commit()
        db.refresh(db_appointment)
    except:
        db.rollback()
        raise

    return db_appointment


def delete_appointment(db: Session, appointment_id: int):
    db_appointment = (
        db.query(models.Appointment)
        .filter(models.Appointment.id == appointment_id)
        .first()
    )

    if not db_appointment:
        return None

    try:
        db.delete(db_appointment)
        db.commit()
    except:
        db.rollback()
        raise

    return db_appointment


def create_patient_record(db: Session, record: schemas.PatientRecordCreate):
    db_record = models.PatientRecord(**record.model_dump())
    try:
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
    except:
        db.rollback()
        raise
    return db_record


def get_patient_records(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.PatientRecord).offset(skip).limit(limit).all()


def update_patient_record(db: Session, record_id: int, record: schemas.PatientRecordCreate):
    db_record = (
        db.query(models.PatientRecord)
        .filter(models.PatientRecord.id == record_id)
        .first()
    )

    if not db_record:
        return None

    for key, value in record.model_dump(exclude_unset=True).items():
        setattr(db_record, key, value)

    try:
        db.commit()
        db.refresh(db_record)
    except:
        db.rollback()
        raise

    return db_record


def delete_patient_record(db: Session, record_id: int):
    db_record = (
        db.query(models.PatientRecord)
        .filter(models.PatientRecord.id == record_id)
        .first()
    )

    if not db_record:
        return None

    try:
        db.delete(db_record)
        db.commit()
    except:
        db.rollback()
        raise

    return db_record