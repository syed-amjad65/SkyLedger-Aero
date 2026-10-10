import os
import random
from typing import Optional
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.orm import declarative_base, sessionmaker, Session

SQLALCHEMY_DATABASE_URL = "sqlite:////tmp/skyledger_aero.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class AircraftModel(Base):
    __tablename__ = "aircraft"
    id = Column(Integer, primary_key=True, index=True)
    tail_number = Column(String, unique=True, index=True)
    model = Column(String)
    station = Column(String, index=True)
    status = Column(String, default="OPERATIONAL")
    downtime_hours = Column(Float, default=0.0)

class PartInventoryModel(Base):
    __tablename__ = "parts"
    id = Column(Integer, primary_key=True, index=True)
    part_number = Column(String, unique=True, index=True)
    description = Column(String)
    part_class = Column(String, index=True)
    station = Column(String, index=True)
    on_hand = Column(Integer)
    min_required = Column(Integer)
    stockout_risk = Column(Float)

class HITLQueueModel(Base):
    __tablename__ = "hitl_queue"
    id = Column(Integer, primary_key=True, index=True)
    action_title = Column(String)
    confidence_score = Column(Float)
    downtime_saved_hours = Column(Float)
    cost_impact = Column(Float)
    status = Column(String, default="PENDING")
    rationale = Column(Text)

app = FastAPI(title="SkyLedger-Aero API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/v1/aog/active")
def get_active_aog(db: Session = Depends(get_db)):
    return db.query(AircraftModel).filter(AircraftModel.status == "AOG").all()

@app.get("/api/v1/inventory/")
def get_inventory(part_class: Optional[str] = None, station: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(PartInventoryModel)
    if part_class:
        query = query.filter(PartInventoryModel.part_class == part_class)
    if station:
        query = query.filter(PartInventoryModel.station == station)
    return query.limit(100).all()

@app.get("/api/v1/hitl/queue")
def get_hitl_queue(db: Session = Depends(get_db)):
    return db.query(HITLQueueModel).filter(HITLQueueModel.status == "PENDING").all()

@app.post("/api/v1/hitl/{item_id}/decision")
def make_hitl_decision(item_id: int, decision: str, db: Session = Depends(get_db)):
    item = db.query(HITLQueueModel).filter(HITLQueueModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item.status = decision.upper()
    db.commit()
    return {"status": "success", "item_id": item_id, "new_status": item.status}
