#  CRUD_API_FOR_MICROSERVICE_USER

Dự án này cung cấp một **API CRUD** cho microservice **User**, được xây dựng bằng **FastAPI**.

---

## Cài đặt môi trường

1️⃣ **Tạo môi trường ảo**  
`python -m venv venv`

2️⃣ **Kích hoạt môi trường ảo**  
- **Windows:** `.\venv\Scripts\activate`  
- **macOS / Linux:** `source venv/bin/activate`

---

## Cài đặt thư viện cần thiết  
`pip install -r requirements.txt`

---

## Chạy ứng dụng  
`uvicorn main:app --reload`

Ứng dụng sẽ chạy mặc định tại địa chỉ:  
[http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Tài liệu API (Swagger UI)  
Sau khi chạy ứng dụng, truy cập:  
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
để xem và thử nghiệm các endpoint của API.

---

## 📚 Thông tin thêm  
- **Framework:** FastAPI  
- **Server:** Uvicorn  
- **Ngôn ngữ:** Python 3.10+
- **sqlalchemy, pydantic[email], psycopg2-binary**
