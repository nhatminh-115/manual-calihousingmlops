FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
#Gunicorn allows multiple flask instances to run at the same time

#Build with docker build -t cali-housing-app:v1 .
#and run with docker run -p 5000:5000 --env-file .env --rm --name cali-test cali-housing-app:v1