# Sử dụng ảnh Python tiêu chuẩn
FROM python:3.10

# Cài đặt các công cụ build C++ bắt buộc cho Fast Downward (g++, cmake, make)
RUN apt-get update && apt-get install -y --no-install-recommends \
    g++ \
    make \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Copy file requirements và cài đặt thư viện Python trước
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn dự án vào container
COPY . .

# --- BƯỚC QUAN TRỌNG: Biên dịch bộ giải Fast Downward cho Linux ---
# Lệnh build chuẩn của Fast Downward (nếu thư mục fd của bác dùng bản chuẩn)
RUN cd /app/solver/fd && ./build.py

# Phân quyền thực thi cho file shell script
RUN chmod +x /app/solver/run_paris.sh

# Cấu hình log không bị delay và phơi cổng PORT
ENV PYTHONUNBUFFERED=1
EXPOSE 8080

# Chạy backend trực tiếp qua main.py
CMD ["python", "backend/main.py"]