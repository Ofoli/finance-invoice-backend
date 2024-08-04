from sqlite3 import Timestamp
from sqlalchemy import Column, DateTime, String, Integer

from ...config.extensions import db, flask_bcrypt


class AuthUser(db.Model):
    __tablename__ = "auth_user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(100))
    fullname = Column(String(255), nullable=False)
    created_on = Column(DateTime, default=Timestamp.now())
    updated_on = Column(DateTime, default=Timestamp.now())

    @password.setter
    def set_password(self, password):
        self.password = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return "<User '{}'>".format(self.email)
