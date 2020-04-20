FROM python:3.4

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

RUN export FLASK_APP=app.py

ENTRYPOINT ["python"]

CMD ["app.py"]
