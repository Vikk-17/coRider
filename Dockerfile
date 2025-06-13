FROM python:slim-bullseye

WORKDIR /coRider

COPY main.py main.py
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt


EXPOSE 3000

CMD ["python", "main.py"]
