from email.policy import default
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from datetime import date, datetime
import uuid

from .connect import Base


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    registered_email = Column(String(64), unique=True, index=True)
    name = Column(String(64), index=True)
    representative = Column(String(64))


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(String(64), default=uuid.uuid1(), primary_key=True, unique=True, index=True)
    name = Column(String(64), index=True)
    course = Column(String(64), index=True)
    org_id = Column(Integer, nullable=False)
    yoc_director = Column(String(64))
    organization = Column(String(64))
    organization_rep = Column(String(64))
    organization_rep_designation = Column(String(64))
    generation_time = Column(String(64), default=str(datetime.now()))
