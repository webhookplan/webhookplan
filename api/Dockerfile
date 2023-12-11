FROM python:3.12.0-alpine

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app

CMD python manage.py collectstatic --noinput && \
    python manage.py migrate && \
    gunicorn --bind 0.0.0.0:8000 --workers=4 core.wsgi
