FROM python:3.9.6-alpine
WORKDIR /app


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apk update \
    && apk add gcc python3-dev musl-dev libffi-dev

ADD requirements.txt /app/requirements.txt

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --upgrade -r requirements.txt

EXPOSE 8080

COPY . /app

ENTRYPOINT ["uvicorn", "app:app","--reload" ,"--host", "0.0.0.0", "--port", "8080"]
