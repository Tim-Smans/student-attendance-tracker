FROM python:3.9

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . ./api

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]
