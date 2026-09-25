import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey, JSON, text
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from app.config.settings import settings
from app.db.session import Base, engine


class Document(Base):
    __tablename__ = "documents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    doc_metadata = Column("metadata", JSON, default=dict)

    chunks = relationship("Chunk", back_populates="document", cascade="all, delete-orphan")


class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String(36), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(settings.EMBEDDING_DIMENSION), nullable=True)
    chunk_index = Column(Integer, nullable=False)
    page = Column(Integer, nullable=True)
    chunk_metadata = Column("metadata", JSON, default=dict)

    document = relationship("Document", back_populates="chunks")


def init_db():
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        conn.commit()
    Base.metadata.create_all(bind=engine)
