FROM python:3.10-bookworm

WORKDIR /app

ADD pyproject.toml /app

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry config virtualenvs.create false 
RUN poetry install 

COPY . /app/
COPY ./start_server.sh /app/

RUN chmod +x start_server.sh

EXPOSE 8000

# CMD ["cd app/ && gunicorn -b :8000 -k uvicorn.workers.UvicornWorker main:app"]