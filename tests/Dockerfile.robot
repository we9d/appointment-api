FROM python:3.10-slim
# อัปเดตและติดตั้ง Chromium (Chrome สำหรับ Linux) และตัว Driver
RUN apt-get update && apt-get install -y chromium chromium-driver
# กำหนดพื้นที่ทำงานภายใน Docker
WORKDIR /tests
# คัดลอกไฟล์ requirements และติดตั้ง
COPY requirements-test.txt .
RUN pip install --no-cache-dir -r requirements-test.txt
# กำหนดคำสั่งเริ่มต้น: สั่งรัน robot และเก็บผลลัพธ์ไว้ที่โฟลเดอร์ results
CMD ["robot", "-d", "results", "."]