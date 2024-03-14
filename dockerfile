from python:3.10.12

RUN apt-get update

WORKDIR usr/src/code_review_1
COPY . .

RUN pip install --no-cache -r requirements.txt

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

CMD python3 manage.py makemigrations && \
    python3 manage.py migrate && \
    python3 manage.py test && \
    python3 manage.py runserver 0.0.0.0:8000