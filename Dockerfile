# ---- Base image ----
FROM python:3.12-slim

# ---- Environment setup ----
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ---- Working directory ----
WORKDIR /app

# ---- Copy dependencies first (for Docker caching) ----
COPY requirements.txt .

# ---- Install Python packages ----
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# ---- Copy the rest of the code ----
COPY . .

# ---- Expose port (Flask runs on 8000 in your code) ----
EXPOSE 8000

# ---- Default environment ----
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# ---- Command to start app ----
CMD ["gunicorn", "-b", "0.0.0.0:8000", "run:app"]
