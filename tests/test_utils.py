from datetime import datetime

import pytest
from back_end.utils import get_string_for_datetime
from back_end.utils import get_datetime_for_string


def test_get_string_for_datetime():
    assert len(get_string_for_datetime()) > 0


def test_get_datetime_for_string():
    s = '2023-02-26 18:02:14'
    d = get_datetime_for_string(s)
    assert type(d) is datetime
