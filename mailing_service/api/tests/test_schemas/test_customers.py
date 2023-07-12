import pytest
from pydantic import ValidationError

from schemas.customers import CustomerCreate


def test_customer_instance_empty():
    with pytest.raises(expected_exception=ValidationError):
        CustomerCreate()


def test_customer_instance_phone_empty():
    with pytest.raises(expected_exception=ValidationError):
        CustomerCreate(
            country_code=7,
            phone_code_id=1,
            timezone_id=1,
        )


def test_customer_instance_phone_wrong():
    with pytest.raises(expected_exception=ValidationError):
        CustomerCreate(
            country_code=7,
            phone_code_id=1,
            phone='phone',
            timezone_id=1,
        )
