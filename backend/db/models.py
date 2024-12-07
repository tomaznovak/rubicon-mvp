from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base

class Papers(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, nullable=False)
    arxiv_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class PDF(Base):
    __tablename__ = "pdfs"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    name = Column(String, nullable=False)
    data = Column(LargeBinary, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class MD(Base):
    __tablename__ = "md"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    name = Column(String, nullable=False)
    data = Column(LargeBinary, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))