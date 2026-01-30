FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY migrations ./migrations
COPY alembic.ini ./alembic.ini

# ✅ 關鍵：讓 Python 能找到 src/cms
ENV PYTHONPATH=/app/src

EXPOSE 8000

CMD ["uvicorn", "cms.main:app", "--host", "0.0.0.0", "--port", "8000"]
