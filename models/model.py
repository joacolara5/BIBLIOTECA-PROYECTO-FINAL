# model.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from .base import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    # Para Flask-Login
    def get_id(self):
        return str(self.id)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False


class Categoria(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    libros = relationship("Libro", back_populates="categoria")


class Libro(Base):
    __tablename__ = "libros"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False)
    autor = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    imagen_url = Column(String(300), nullable=True)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=True)

    categoria = relationship("Categoria", back_populates="libros")
