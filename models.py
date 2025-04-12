from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DECIMAL, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB, HSTORE
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
from datetime import datetime
from pytz import timezone

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    full_name = Column(String(100))
    email = Column(String(100), unique=True, nullable=False)
    role = Column(String(20), nullable=False)
    created_at = Column(TIMESTAMP, default=lambda: datetime.now(vietnam_tz))

class Transaction(Base):
    __tablename__ = 'transactions'

    transaction_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete="SET NULL"))
    card_number = Column(String(20), nullable=False)
    transaction_time = Column(TIMESTAMP, default=datetime.utcnow)
    location = Column(String(255))
    amount = Column(DECIMAL(10, 2), nullable=False)
    transaction_type = Column(String(20), nullable=False)
    is_fraud = Column(Boolean, default=False)
    transaction_metadata = Column(HSTORE)  # <-- Đổi tên ở đây

class FraudReport(Base):
    __tablename__ = 'fraud_reports'

    report_id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey('transactions.transaction_id', ondelete="CASCADE"))
    reported_by = Column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"))
    report_reason = Column(Text, nullable=False)
    report_time = Column(TIMESTAMP, default=datetime.utcnow)
    status = Column(String(20), default='pending')
    details = Column(JSONB)

vietnam_tz = timezone('Asia/Ho_Chi_Minh')

class News(Base):
    __tablename__ = 'news'

    news_id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"))
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=lambda: datetime.now(vietnam_tz))

class KnowledgeBase(Base):
    __tablename__ = 'knowledge_base'

    knowledge_id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"))
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=lambda: datetime.now(vietnam_tz))
