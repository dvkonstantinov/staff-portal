FROM python:3.9-slim
WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY . /app
RUN pip3 install -r /app/requirements.txt --no-cache-dir
CMD ["gunicorn", "portal.wsgi:application", "--bind", "0:8001" ]
#CMD ["python3", "manage.py", "runserver", "0:8001"]