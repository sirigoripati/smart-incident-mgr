
import os

SLACK_WEBHOOK = os.getenv("SIMS_SLACK_WEBHOOK_URL", "").strip()
POLL_INTERVAL_SECONDS = int(os.getenv("SIMS_POLL_INTERVAL_SECONDS", "30"))
LATENCY_THRESHOLD_MS = int(os.getenv("SIMS_LATENCY_THRESHOLD_MS", "1500"))
DATABASE_URL = os.getenv("SIMS_DATABASE_URL", "sqlite:///./sims.db")
