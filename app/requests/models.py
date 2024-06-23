from enum import Enum
import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.databases.database import Base


class Affinity(str, Enum):
    OSCURIDAD = "Oscuridad"
    LUZ = "Luz"
    FUEGO = "Fuego"
    AGUA = "Agua"
    VIENTO = "Viento"
    TIERRA = "Tierra"


class RequestStatus(str, Enum):
    PENDING = "Pendiente"
    APPROVED = "Aprobado"
    REJECTED = "Rechazado"


class Grimorio(Base):
    __tablename__ = 'grimorios'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tipo_trebol = Column(Integer, nullable=False)
    ponderacion = Column(Integer, nullable=False)
    name = Column(String, nullable=False)

    requests = relationship("Request", back_populates="grimorio")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Request(Base):
    __tablename__ = 'requests'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    identification = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    affinity = Column(String, nullable=False)
    status = Column(String, nullable=False, default=RequestStatus.PENDING)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    grimorio_id = Column(String, ForeignKey('grimorios.id'))
    grimorio = relationship("Grimorio", back_populates="requests")

    def __init__(self, **kwargs):
        if 'id' not in kwargs:
            kwargs['id'] = str(uuid.uuid4())
        super().__init__(**kwargs)
