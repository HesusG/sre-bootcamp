FROM python:3-alpine

# Add your instructions to dockerize the application
# App must run on port 8000
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["python", "api.py"]