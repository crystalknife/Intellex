# Intellex Backend
#
# Single-stage build -- there's no compiled-artifact-vs-runtime split
# worth doing here the way there is for the Next.js frontend; the
# Python dependencies (including spacy's en_core_web_sm model) are the
# runtime, not an intermediate build product.

FROM python:3.13-slim

WORKDIR /app

# Minimal system deps: psycopg (Postgres driver) needs libpq at runtime;
# build-essential is needed only transiently for any package without a
# prebuilt wheel for this platform, then removed in the same layer to
# keep the final image small.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt ./requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Copied so the existing `from backend.app...` import convention used
# throughout the codebase resolves correctly from /app as the working
# directory, without needing uvicorn's --app-dir flag.
COPY backend ./backend

EXPOSE 8000

# --proxy-headers: this sits behind a reverse proxy/load balancer in
# every real deployment target (Railway, Render, Fly, nginx) -- without
# it, uvicorn would log/see the proxy's IP instead of the real client,
# and would not trust the proxy's X-Forwarded-Proto for HTTPS detection.
CMD ["uvicorn", "backend.app.api.app:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
