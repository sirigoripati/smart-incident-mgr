
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Incident
from ..schemas import IncidentOut

router = APIRouter(prefix="/api/incidents", tags=["incidents"])

@router.get("", response_model=List[IncidentOut])
def list_incidents(db: Session = Depends(get_db)):
    return db.query(Incident).order_by(Incident.created_at.desc()).limit(200).all()
