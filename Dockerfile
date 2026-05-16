# ==========================================
# GIAI ĐOẠN 1: BUILDER (Dùng bản full để biên dịch C++)
# ==========================================
FROM python:3.10 AS builder

WORKDIR /app
COPY . .

# Cài đặt các công cụ biên dịch thiết yếu
RUN apt-get update && apt-get install -y g++ make cmake git

# Thực hiện biên dịch Fast Downward thành file chạy
WORKDIR /app/solver/fd
RUN python3 build.py

# ==========================================
# GIAI ĐOẠN 2: RUNTIME (Chạy ứng dụng chính thức)
# ==========================================
FROM python:3.10 AS runtime

WORKDIR /app

# Copy toàn bộ dữ liệu đã được build từ giai đoạn builder sang
COPY --from=builder /app /app

# Cài đặt các thư viện Python cho Backend FastAPI/Uvicorn
RUN pip install --no-cache-dir -r backend/requirements.txt

# Cấp quyền thực thi cho cả 2 file script shell trong thư mục solver
RUN chmod +x /app/solver/solve.sh
RUN chmod +x /app/solver/run_paris.sh

# Cổng mở của ứng dụng
EXPOSE 10000

# Chạy Backend chính thức từ thư mục gốc /app
CMD ["python3", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "10000"]