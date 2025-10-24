
import asyncio
from fastapi import FastAPI
from .database import Base, engine
from .routers import services, incidents
from .monitor import monitor_loop

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Incident Management System", version="0.1.0")
app.include_router(services.router)
app.include_router(incidents.router)

@app.on_event("startup")
async def startup_event():
    # Launch background monitor
    loop = asyncio.get_event_loop()
    loop.create_task(monitor_loop())

@app.get("/")
def root():
    return {"ok": True, "service": "SIMS"}
