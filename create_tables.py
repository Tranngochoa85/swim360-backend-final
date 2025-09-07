# File: create_tables.py (Phiên bản cuối cùng, tường minh)

from app.database import Base, engine

# Import TƯỜNG MINH từng model để đảm bảo chúng được đăng ký với Base
from app.models.user import User
from app.models.coach_profile import CoachProfile
from app.models.document import Document
from app.models.pool import Pool
from app.models.booking import Booking
from app.models.transaction import Transaction

print("Forcing SQLAlchemy to recognize all models...")
print("Connecting to the database to create tables...")

# Ra lệnh cho SQLAlchemy tạo tất cả các bảng mà nó đã "nhìn thấy"
Base.metadata.create_all(bind=engine)

print("Tables should now be created. Please check Supabase.")