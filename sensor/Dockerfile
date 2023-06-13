FROM postgres as postgres_sensor
ENV POSTGRES_DB sensors
COPY psql_dump.sql /docker-entrypoint-initdb.d/

FROM python:3 as sensor
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
CMD ["python", "app.py"]
