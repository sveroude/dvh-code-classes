import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class CodeClass(Base):
    __tablename__ = 'code_class'

    title = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    speaker = Column(String(50))
    date = Column(String(20))
    description = Column(String(800))

# Open a connection to the database by creating an SQLEngine object
engine = create_engine('sqlite:///codeclasses.db')
# Create the initial database
Base.metadata.create_all(engine)
