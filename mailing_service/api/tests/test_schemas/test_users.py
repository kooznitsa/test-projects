import pytest
from pydantic import ValidationError

from schemas.users import User


# def test_user_instance_empty():
#     with pytest.raises(expected_exception=ValidationError):
#         User()


def test_user_password_hash(user_to_create):
    user = user_to_create

    assert isinstance(user.password_hash, str)
    assert user.verify_password('qwerty') is True
