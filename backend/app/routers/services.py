
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Service
from ..schemas import ServiceCreate, ServiceOut

router = APIRouter(prefix="/api/services", tags=["services"])

@router.post("", response_model=ServiceOut)
def create_service(payload: ServiceCreate, db: Session = Depends(get_db)):
    exists = db.query(Service).filter(Service.name == payload.name).first()
    if exists:
        raise HTTPException(status_code=409, detail="Service name already exists")
    svc = Service(name=payload.name, url=str(payload.url), expected_status=payload.expected_status)
    db.add(svc)
    db.commit()
    db.refresh(svc)
    return svc

@router.get("", response_model=List[ServiceOut])
def list_services(db: Session = Depends(get_db)):
    return db.query(Service).order_by(Service.created_at.desc()).all()

@router.delete("/{service_id}", status_code=204)
def delete_service(service_id: int, db: Session = Depends(get_db)):
    svc = db.query(Service).get(service_id)
    if not svc:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(svc)
    db.commit()
    return
