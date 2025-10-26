# crud.py
from sqlalchemy.orm import Session
from uuid import UUID
import models, schemas

# --- CRUD CHO USER ---

def get_user(db: Session, user_id: UUID):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: UUID, user_in: schemas.UserUpdate):
    db_user = get_user(db, user_id=user_id)
    if not db_user:
        return None
    
    # Lấy dữ liệu từ Pydantic model, chỉ cập nhật các trường được gửi
    update_data = user_in.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_user, key, value)
        
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: UUID):
    db_user = get_user(db, user_id=user_id)
    if not db_user:
        return None
    
    db.delete(db_user)
    db.commit()
    return db_user

def create_user(db: Session, user: schemas.UserCreate):
    # Tạo user KHÔNG có mật khẩu.
    # Dịch vụ auth của bạn sẽ chịu trách nhiệm 'cập nhật'
    # cột password_hash sau đó.
    db_user = models.User(
        email=user.email,
        full_name=user.full_name,
        phone_number=user.phone_number,
        role='passenger' # Mặc định
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- CRUD CHO DRIVER PROFILE ---

def create_driver_profile(db: Session, profile: schemas.DriverProfileCreate, user_id: UUID):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()

    if not db_user:
        return None 

    profile_data = profile.dict() 
    
    db_profile = models.DriverProfile(**profile_data, user_id=user_id)
    db.add(db_profile)


    db_user.role = "driver"
    db.add(db_user)# Thông báo cho session biết là object này đã thay đổi

    try:
        db.commit()
        db.refresh(db_profile) # Làm mới để lấy dữ liệu từ CSDL (như ID mới)
    except Exception as e:
        db.rollback() # Hoàn tác nếu có lỗi
        raise e
    
    return db_profile

def get_driver_profile(db: Session, profile_id: UUID):
    return db.query(models.DriverProfile).filter(models.DriverProfile.driver_id == profile_id).first()

def get_driver_profile_by_user_id(db: Session, user_id: UUID):
    return db.query(models.DriverProfile).filter(models.DriverProfile.user_id == user_id).first()

def update_driver_profile(db: Session, profile_id: UUID, profile_in: schemas.DriverProfileUpdate):
    db_profile = get_driver_profile(db, profile_id=profile_id)
    if not db_profile:
        return None
    
    update_data = profile_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_profile, key, value)
        
    db.commit()
    db.refresh(db_profile)
    return db_profile

def delete_driver_profile(db: Session, profile_id: UUID):
    db_profile = get_driver_profile(db, profile_id=profile_id)
    if not db_profile:
        return None
    
    db.delete(db_profile)
    db.commit()
    return db_profile

# --- PHẦN MỚI CHO VEHICLE (TOÀN BỘ) ---

def create_vehicle(db: Session, vehicle: schemas.VehicleCreate, driver_id: UUID):
    # models.Vehicle sẽ tự tạo UUID cho 'id'
    db_vehicle = models.Vehicle(
        **vehicle.dict(), 
        driver_id=driver_id
    )
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

def get_vehicle(db: Session, vehicle_id: UUID):
    return db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()

def get_vehicles_by_driver(db: Session, driver_id: UUID, skip: int = 0, limit: int = 100):
    return db.query(models.Vehicle)\
             .filter(models.Vehicle.driver_id == driver_id)\
             .offset(skip)\
             .limit(limit)\
             .all()

def update_vehicle(db: Session, vehicle_id: UUID, vehicle_in: schemas.VehicleUpdate):
    db_vehicle = get_vehicle(db, vehicle_id=vehicle_id)
    if not db_vehicle:
        return None
    
    update_data = vehicle_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_vehicle, key, value)
        
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

def delete_vehicle(db: Session, vehicle_id: UUID):
    db_vehicle = get_vehicle(db, vehicle_id=vehicle_id)
    if not db_vehicle:
        return None
    
    db.delete(db_vehicle)
    db.commit()
    return db_vehicle
