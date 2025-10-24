
import asyncio, time
import http.client
from urllib.parse import urlparse
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Service, Incident
from .settings import POLL_INTERVAL_SECONDS, LATENCY_THRESHOLD_MS
from .alerts import post_slack

async def poll_once():
    db: Session = SessionLocal()
    try:
        services = db.query(Service).filter(Service.is_active == True).all()
        for svc in services:
            t0 = time.perf_counter()
            status = None
            msg = None
            try:
                u = urlparse(svc.url)
                conn = http.client.HTTPSConnection(u.netloc, timeout=5)
                path = u.path or "/"
                if u.query:
                    path += "?" + u.query
                conn.request("GET", path)
                resp = conn.getresponse()
                status = resp.status
                resp.read()
                conn.close()
            except Exception as e:
                msg = f"Request error: {e}"
            latency_ms = (time.perf_counter() - t0) * 1000.0
            bad = (status is None) or (status != svc.expected_status) or (latency_ms > LATENCY_THRESHOLD_MS)

            if bad:
                inc = Incident(service_id=svc.id, status_code=status, latency_ms=latency_ms, message=msg)
                db.add(inc)
                db.commit()
                post_slack(f":rotating_light: Incident on *{svc.name}* — status={status}, latency={latency_ms:.0f}ms, url={svc.url}")
    finally:
        db.close()

async def monitor_loop():
    while True:
        await poll_once()
        await asyncio.sleep(POLL_INTERVAL_SECONDS)
