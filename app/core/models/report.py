from datetime import datetime, timedelta

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship


from . import BaseModel


def default_previous_month():
    today = datetime.today()
    first_day_this_month = today.replace(day=1)
    last_day_previous_month = first_day_this_month - timedelta(days=1)
    return last_day_previous_month.replace(day=1)


class BaseReport(BaseModel):
    __abstract__ = True

    total_pages = Column(Integer, nullable=False)
    month = Column(DateTime, nullable=False, default=default_previous_month())


class ApiReport(BaseReport):
    __tablename__ = "api_report"

    user_id = Column(Integer, ForeignKey("api_client.id"), nullable=False, index=True)
    network = Column(String(100), nullable=False)

    user = relationship("ApiClient")

    __table_args__ = (Index("apidx_user_id_month", "user_id", "month"),)


class BlastReport(BaseReport):
    __tablename__ = "blast_report"

    user_id = Column(Integer, ForeignKey("blast_client.id"), nullable=False, index=True)
    message = Column(String, nullable=False)
    sent_date = Column(DateTime, nullable=False)
    sender = Column(String(100), nullable=False)

    user = relationship("BlastClient")

    __table_args__ = (Index("blastix_user_id_month", "user_id", "month"),)


class EsmeReport(BaseReport):
    __tablename__ = "esme_report"

    user_id = Column(Integer, ForeignKey("esme_client.id"), nullable=False, index=True)
    network = Column(String(100), nullable=False)

    user = relationship("ESMEClient")

    __table_args__ = (Index("esmeix_user_id_month", "user_id", "month"),)


class BaseEmailReport(BaseModel):
    __abstract__ = True

    sent = Column(Integer, default=0)
    failed = Column(Integer, default=0)
    opened = Column(Integer, default=0)
    clicked = Column(Integer, default=0)
    bounced = Column(Integer, default=0)
    rejected = Column(Integer, default=0)
    complaint = Column(Integer, default=0)
    delivered = Column(Integer, default=0)
    month = Column(DateTime, nullable=False, default=default_previous_month())


class ApiEmailReport(BaseEmailReport):
    __tablename__ = "email_api_report"

    user_id = Column(Integer, ForeignKey("api_client.id"), nullable=False, index=True)
    user = relationship("ApiClient")

    __table_args__ = (Index("email_apidx_user_id_month", "user_id", "month"),)


class WebEmailReport(BaseEmailReport):
    __tablename__ = "email_web_report"

    user_id = Column(Integer, ForeignKey("api_client.id"), nullable=False, index=True)
    user = relationship("ApiClient")

    __table_args__ = (Index("email_webidx_user_id_month", "user_id", "month"),)
