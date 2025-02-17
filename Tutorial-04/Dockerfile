FROM python:3.11

WORKDIR /app

RUN python -m pip install --upgrade pip

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "main:app"]
