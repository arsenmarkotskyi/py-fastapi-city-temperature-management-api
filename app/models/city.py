from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, max_length=100)
    additional_info = Column(String, nullable=True)

    temperatures = relationship(
        "Temperature", 
        back_populates="city",
        cascade="all, delete-orphan"
    )