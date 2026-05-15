FROM python:3.10-slim

# Cài đặt công cụ biên dịch
RUN apt-get update && apt-get install -y \
    g++ make cmake git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Biên dịch Fast Downward
WORKDIR /app/solver/fd
RUN python3 build.py

# Cài đặt thư viện cho Backend
WORKDIR /app
RUN pip install --no-cache-dir -r backend/requirements.txt

# Render dùng cổng 10000 mặc định hoặc bạn có thể config 8000
EXPOSE 8000
RUN chmod +x /app/solver/run_paris.sh
# Chạy backend
CMD ["python3", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]