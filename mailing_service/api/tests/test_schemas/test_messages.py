from datetime import datetime, time

import pytest
from pydantic import ValidationError

from schemas.messages import MessageCreate


def test_message_instance_empty():
    with pytest.raises(expected_exception=ValidationError):
        MessageCreate()


def test_message_instance_text_message_empty():
    with pytest.raises(expected_exception=ValidationError):
        MessageCreate(
            mailout_id=1,
            customer_id=1,
        )
