# veritabanı ile bağlantı yapılacak - fastapi sql dökümantasyon
# sql tabanlı veritabanlarıyla çalışırken baglantı kurmak için kullanılan kütüphane - sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./tarifai_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()  # Modelerimizi oluştururken kullanıcaz