from time import timezone
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID, ARRAY
import uuid
from datetime import datetime, timezone
import enum
from ..database.core import Base

class Priority(enum.Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2

class Todo(Base):
    __tablename__ = "todos"
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"),  nullable=False,)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    priority = Column(Enum(Priority), nullable=False, default=Priority.MEDIUM)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    def __repr__(self):
        return f"Todo(id={self.id}, user_id={self.user_id}, title={self.title}, description={self.description}, completed={self.completed}, priority={self.priority}, created_at={self.created_at}, updated_at={self.updated_at})"