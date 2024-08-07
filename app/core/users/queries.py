from typing import Optional, Dict, List
from ..models.user import AuthUser


def get_all_users() -> List[AuthUser]:
    return AuthUser.query.all()


def get_user(id: int) -> Optional[AuthUser]:
    return AuthUser.query.get(ident=id)


def get_user_by_email(email: str) -> Optional[AuthUser]:
    return AuthUser.query.filter_by(email=email).first()


def create_user(data: Dict) -> AuthUser:
    new_user = AuthUser(**data)
    new_user.set_password(data.get("password"))
    new_user.save()
    return new_user
