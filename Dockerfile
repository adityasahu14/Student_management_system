FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./

RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "edutrack.wsgi:application", "--bind", "0.0.0.0:8000"]
