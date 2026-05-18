# Sử dụng trực tiếp ảnh Python có sẵn bộ build GCC/G++ (Không cần apt-get install g++ nữa)
FROM python:3.10-bullseye

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Khởi tạo môi trường cơ bản
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Copy file requirements và cài đặt thư viện Python trước để tận dụng cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn của dự án (bao gồm backend, solver, frontend/dist) vào container
COPY . .

# Phân quyền thực thi cho file solve.sh trên Linux
RUN chmod +x /app/solver/solve.sh

# Cấu hình log không bị delay
ENV PYTHONUNBUFFERED=1

# Railway tự động cấp PORT
EXPOSE 8080

# Chạy backend qua main.py
CMD ["python", "backend/main.py"]