FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE drf.settings

RUN mkdir /app
WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "drf.wsgi:application", "--bind", "0.0.0.0:8000"]
