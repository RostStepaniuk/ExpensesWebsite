FROM python:3.10.12

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install requirements.txt

COOPY ./django_project /app

WORKDIR /app

COPY ./entrypoint.sh /
ENTRYPOINT [ "sh", "entrypoint.sh" ]