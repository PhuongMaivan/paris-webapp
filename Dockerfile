# Sử dụng ảnh Python tiêu chuẩn
FROM python:3.10

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Copy file requirements và cài đặt thư viện Python trước
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn dự án (bao gồm cả thư mục solver/fd đã build sẵn từ local) vào container
COPY . .

# Phân quyền thực thi cho file shell script và các công cụ thực thi trong fd nếu có
RUN chmod +x /app/solver/run_paris.sh

# Cấu hình log không bị delay và phơi cổng PORT
ENV PYTHONUNBUFFERED=1
EXPOSE 8080

# Chạy backend trực tiếp qua main.py
CMD ["python", "backend/main.py"]