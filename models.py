#veritabanında tutulacak tablolar oluşturulacak. Kolonlar vs.
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Table
from datetime import datetime

# Malzeme ve tarif arasındaki ilişki tablosu
material_recipe = Table('material_recipe',
    Base.metadata,
    Column('material_id', Integer, ForeignKey('materials.id'), primary_key=True),
    Column('recipe_id', Integer, ForeignKey('recipes.id'), primary_key=True)
)

class Materials(Base):
    __tablename__ ='materials'

    id = Column(Integer, primary_key=True, index=True)
    material_name = Column(String, nullable=False)
    isExpiring = Column(Boolean, default=False)
    ExpirationDate = Column(DateTime)
    owner_id = Column(Integer, ForeignKey('users.id')) #Malzemeler hangi kullanıcıya ait olduğunu
                                                       #Yabancı anahtar kullanarak ilişki kurduk. Bire çok ilişki
    owner = relationship("User", backref="materials")
    recipes = relationship("Recipe", secondary=material_recipe, back_populates="materials")

class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)  # Tarif adı
    description = Column(String)            # Tarifin açıklaması
    instructions = Column(String)           # Nasıl yapılır?
    created_by = Column(Integer, ForeignKey('users.id'))  # Tarifi ekleyen kullanıcı
    created_at = Column(DateTime, default=datetime.now)   # Tarifin oluşturulma tarihi

    user = relationship("User", backref="recipes")  # Bire-çok ilişki
    materials = relationship("Materials", secondary=material_recipe, back_populates="recipes")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True,nullable=False)  #aynı emaille başka biri kayıt olmasın dedik
    username = Column(String, unique=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String, nullable=False)   #Şifrelenmiş parola
    is_active = Column(Boolean, default=True)
    role = Column(String)
    phone_number = Column(String)

# nullable=False alanlar boş geçilmesin