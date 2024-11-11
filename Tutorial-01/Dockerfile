FROM python:3.11

WORKDIR /app

COPY ./requiments.txt ./requiments.txt

RUN python3 -m pip install --upgrade pip

RUN pip install -r requiments.txt

COPY ./app/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]