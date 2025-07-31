FROM python:3.11-slim

WORKDIR /app
COPY . .
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app
COPY ./artifacts ./artifacts
COPY prestart.sh ./prestart.sh

CMD ["python", "main.py"]

# RUN chmod +x prestart.sh
# CMD ["./prestart.sh"]