# Sử dụng ảnh Python tiêu chuẩn
FROM python:3.10

# Cài đặt công cụ giải nén unzip cho Linux
RUN apt-get update && apt-get install -y unzip && rm -rf /var/lib/apt/lists/*

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Copy file requirements và cài đặt thư viện Python trước
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy file nén solver và toàn bộ code vào
COPY . .

# Tiến hành giải nén file solver.zip đè thẳng vào container để giữ nguyên file chạy
RUN unzip -o solver.zip -d . && rm solver.zip

# Phân quyền thực thi cho file shell script và các công cụ thực thi
RUN chmod +x /app/solver/run_paris.sh

# Cấu hình log không bị delay và phơi cổng PORT
ENV PYTHONUNBUFFERED=1
EXPOSE 8080

# Chạy backend trực tiếp qua main.py
CMD ["python", "backend/main.py"]