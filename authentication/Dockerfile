FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt


EXPOSE 5002

COPY . .

CMD ["python", "main.py"]