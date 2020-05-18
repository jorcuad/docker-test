FROM python:3.7

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

RUN export FLASK_APP=wsgi.py

ENTRYPOINT ["flask"]

CMD ["run"]
