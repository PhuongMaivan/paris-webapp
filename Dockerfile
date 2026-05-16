FROM python:3.10

# 1. Cài đặt các công cụ biên dịch C++ thiết yếu cho Linux
RUN apt-get update && apt-get install -y \
    g++ make cmake git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# 2. Biên dịch trực tiếp Fast Downward trên chính môi trường này (Không lo gãy symlink)
WORKDIR /app/solver/fd
RUN python3 build.py

# 3. Cài đặt các thư viện Python cho Backend từ thư mục gốc
WORKDIR /app
RUN pip install --no-cache-dir -r backend/requirements.txt

# 4. Cấp quyền thực thi cho cả 2 file script shell
RUN chmod +x /app/solver/solve.sh
RUN chmod +x /app/solver/run_paris.sh

# Render dùng cổng 10000 mặc định
EXPOSE 10000

# Chạy backend chính thức
CMD ["python3", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "10000"]