FROM python:slim-bullseye

WORKDIR /coRider

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY main.py main.py

EXPOSE 3000

CMD ["python", "main.py"]
