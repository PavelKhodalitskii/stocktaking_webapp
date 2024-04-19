from python:3.10.12

RUN apt-get update

WORKDIR inventory_checking
COPY . .

RUN pip install --no-cache -r requirements.txt

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

CMD python3 manage.py makemigrations account && \
    python3 manage.py makemigrations items_management && \
    python3 manage.py makemigrations licences_management && \
    python3 manage.py migrate --run-syncdb && \
    # python3 manage.py test && \
    python3 manage.py runserver 0.0.0.0:8000