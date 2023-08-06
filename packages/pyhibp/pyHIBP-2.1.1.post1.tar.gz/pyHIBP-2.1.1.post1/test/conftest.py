import pytest

import pyHIBP


@pytest.fixture(autouse=True)
def dev_user_agent(monkeypatch):
    ua_string = pyHIBP.pyHIBP_USERAGENT
    monkeypatch.setattr(pyHIBP, 'pyHIBP_USERAGENT', ua_string + " (Testing Suite)")
