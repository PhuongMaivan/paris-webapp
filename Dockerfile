# Sử dụng Python làm base image (chọn phiên bản phù hợp, ví dụ 3.10 hoặc 3.11)
FROM python:3.10-slim

# Cài đặt các công cụ hệ thống cần thiết cho Fast Downward và bộ giải (g++, make, cmake, bash...)
RUN apt-get update && apt-get install -y --no-install-recommends \
    g++ \
    make \
    cmake \
    bash \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Copy file quản lý thư viện Python và cài đặt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn dự án vào container (bao gồm backend, solver, và frontend)
COPY . .

# Đảm bảo phân quyền thực thi cho file solve.sh bên trong môi trường Linux Container
RUN chmod +x /app/solver/solve.sh

# Cấu hình biến môi trường để Python không ghi file pyc và log được in ra lập tức
ENV PYTHONUNBUFFERED=1

# Railway sẽ tự động cấp cổng thông qua biến PORT, mặc định dự phòng là 8080
EXPOSE 8080

# Lệnh khởi chạy Uvicorn server (gọi trực tiếp file main.py để tự động ăn biến PORT)
CMD ["python", "backend/main.py"]