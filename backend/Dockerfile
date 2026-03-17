FROM python:3.11-slim
WORKDIR /backend
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
COPY wait-for-it.sh .
RUN chmod +x wait-for-it.sh
CMD ["./wait-for-it.sh", "db:3306", "--", "python3", "server.py"]