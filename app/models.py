from sqlalchemy.sql import func
from sqlalchemy import (
    ARRAY,
    String,
    Column,
    Integer,
    DateTime,
    LargeBinary,
)


from .database import Base

class Files(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    file_title = Column(String, nullable=True)
    output_outline = Column(String, nullable=True)
    output_keyword = Column(ARRAY(String), nullable=True)
    output_keyword_float = Column(ARRAY(String), nullable=True)
    output_pic = Column(ARRAY(String), nullable=True)
    input_time = Column(DateTime(timezone=True), server_default=func.now())