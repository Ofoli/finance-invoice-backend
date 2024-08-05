import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, String, Integer
from sqlalchemy.ext.declarative import declared_attr

from ...config.extensions import db, flask_bcrypt


class Base(db.Model):
    __abstract__ = True

    @declared_attr
    def created_at(cls):
        return Column(
            DateTime, default=datetime.datetime.now(datetime.UTC), nullable=False
        )

    @declared_attr
    def updated_at(cls):
        return Column(
            DateTime,
            default=datetime.datetime.now(datetime.UTC),
            onupdate=datetime.datetime.now(datetime.UTC),
            nullable=False,
        )

    def save(self):
        db.session.add(self)
        db.session.commit()


class AuthUser(Base):
    __tablename__ = "auth_user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(100))
    fullname = Column(String(255), nullable=False)

    def set_password(self, password):
        self.password = flask_bcrypt.generate_password_hash(
            password).decode("utf-8")

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return "<User '{}'>".format(self.email)


class BasePostpaidClient(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False, unique=True)
    rate = Column(Float, nullable=False)


class ApiClient(BasePostpaidClient):
    __tablename__ = "api_client"

    aid = Column(Integer, nullable=False)


class BlastClient(BasePostpaidClient):
    __tablename__ = "blast_client"

    user_id = Column(Integer, nullable=False)
    reseller_id = Column(Integer, nullable=False)
    is_reseller = Column(Boolean, default=False)


class ESMEClient(BasePostpaidClient):
    __tablename__ = "esme_client"
