FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOME=/home/appuser \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY config_loader.py config_init.py mqtt_store.py streamlit_app.py collector.py ./

RUN mkdir -p /data /home/appuser/.streamlit && \
    chown -R 65532:65532 /data /app /home/appuser
USER 65532:65532

EXPOSE 8080
HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/_stcore/health')"
CMD ["streamlit", "run", "streamlit_app.py", "--server.address=0.0.0.0", "--server.port=8080", "--server.headless=true"]

