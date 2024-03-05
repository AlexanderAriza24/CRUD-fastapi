FROM python:latest

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

EXPOSE 80

ENV GOOGLE_APPLICATION_CREDENTIALS = /code/app/bd-prueba-persona-taller-firebase-adminsdk-1xt6v-6ac6a954ae.json

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]