FROM python:slim

WORKDIR /app

ADD requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

ADD . /app

EXPOSE 80
EXPOSE 5000

CMD ["python", "app.py", "--host=172.18.0.6"]