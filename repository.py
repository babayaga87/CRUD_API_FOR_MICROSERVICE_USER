# repository.py
from sqlalchemy.orm import Session
from . import models, schemas

# -----------------
# LƯU Ý QUAN TRỌNG:
# Bạn PHẢI dùng thư viện như 'passlib' để hash password thật.
# Đây chỉ là ví dụ đơn giản.
def get_password_hash(password):
    return password + "_super_hashed" # KHÔNG DÙNG CÁCH NÀY TRONG THỰC TẾ
# -----------------


def get_user_by_email(db: Session, email: str):
    """
    Hàm lấy user bằng email (dùng để kiểm tra trùng lặp)
    """
    return db.query(models.User).filter(models.User.email == email).first()


def get_user(db: Session, user_id: int):
    """
    Hàm lấy user bằng ID
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: schemas.UserCreate):
    """
    Hàm tạo user mới
    """
    # 1. Hash password (Quan trọng!)
    hashed_password = get_password_hash(user.password)
    
    # 2. Tạo đối tượng model SQLAlchemy
    db_user = models.User(
        email=user.email, 
        hashed_password=hashed_password
    )
    
    # 3. Thêm vào session và lưu
    db.add(db_user)
    db.commit()
    db.refresh(db_user) # Lấy lại data mới (ví dụ ID do CSDL tự tạo)
    
    return db_user