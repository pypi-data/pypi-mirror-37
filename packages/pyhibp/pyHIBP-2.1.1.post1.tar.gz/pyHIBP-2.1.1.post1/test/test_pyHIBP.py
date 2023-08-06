import time

import pytest

import pyHIBP


TEST_ACCOUNT = "test@example.com"
TEST_DOMAIN = "adobe.com"
TEST_DOMAIN_NAME = "Adobe"
# Very likely to not exist; SHA-1 hash of the SHA-1 hash of the string "password"
TEST_NONEXISTENT_ACCOUNT_NAME = "353e8061f2befecb6818ba0c034c632fb0bcae1b"


@pytest.fixture(autouse=True)
def rate_limit():
    # The HIBP API has a rate-limit of 1500ms. Sleep for 2 seconds between each test.
    time.sleep(2)


class TestGetBreaches(object):
    def test_get_breaches_account(self):
        # get_account_breaches(account=TEST_ACCOUNT, domain=None, truncate_response=False, include_unverified=False):
        resp = pyHIBP.get_account_breaches(account=TEST_ACCOUNT)
        assert isinstance(resp, list)
        # As of a manual test, there were 46 accounts for the test@example.com; so >=20 is safe.
        assert len(resp) >= 20
        assert isinstance(resp[0], dict)

    def test_get_breaches_account_with_domain(self):
        # get_account_breaches(account=TEST_ACCOUNT, domain=TEST_DOMAIN, truncate_response=False, include_unverified=False):
        resp = pyHIBP.get_account_breaches(account=TEST_ACCOUNT, domain=TEST_DOMAIN)
        assert isinstance(resp, list)
        # We're limiting the domain; so we only expect one breach to be returned
        assert len(resp) == 1
        assert isinstance(resp[0], dict)
        assert resp[0]['Name'] == TEST_DOMAIN_NAME

    def test_get_breaches_account_with_truncation(self):
        # get_account_breaches(account=TEST_ACCOUNT, domain=None, truncate_response=True, include_unverified=False):
        resp = pyHIBP.get_account_breaches(account=TEST_ACCOUNT, truncate_response=True)
        assert isinstance(resp, list)
        assert len(resp) >= 20
        assert isinstance(resp[0], dict)
        # The individual dicts are only the name of the breached website (since we're truncating)
        item = resp[0]
        assert len(item) == 1
        assert 'Name' in item
        assert 'DataClasses' not in item

    def test_get_breaches_retrieve_all_breaches_with_unverified(self):
        # get_account_breaches(account=TEST_ACCOUNT, domain=None, truncate_response=False, include_unverified=True):
        resp = pyHIBP.get_account_breaches(account=TEST_ACCOUNT, include_unverified=True)
        assert isinstance(resp, list)
        assert len(resp) > 50
        has_unverified = False
        for item in resp:
            if not item['IsVerified']:
                has_unverified = True
                # If we see any unverified items, that's enough.
                break
        assert has_unverified

    def test_get_breaches_return_false_if_no_accounts(self):
        # get_account_breaches(account=TEST_PASSWORD_SHA1_HASH, domain=None, truncate_response=False, include_unverified=False):
        resp = pyHIBP.get_account_breaches(account=TEST_NONEXISTENT_ACCOUNT_NAME)
        assert not resp
        assert isinstance(resp, bool)

    def test_get_breaches_raise_if_account_is_not_specified(self):
        # get_account_breaches(account=1, domain=None, truncate_response=False, include_unverified=False):
        with pytest.raises(AttributeError) as excinfo:
            # Will raise because the account must be a string (specifically, six.text_type)
            pyHIBP.get_account_breaches(account=None)
        assert "The account parameter must be specified, and must be a string" in str(excinfo.value)

    def test_get_breaches_raise_if_account_is_not_string(self):
        # get_account_breaches(account=1, domain=None, truncate_response=False, include_unverified=False):
        with pytest.raises(AttributeError) as excinfo:
            # Will raise because the account must be a string (specifically, six.text_type)
            pyHIBP.get_account_breaches(account=1)
        assert "The account parameter must be specified, and must be a string" in str(excinfo.value)

    def test_get_breaches_raise_if_domain_is_not_string(self):
        # get_account_breaches(account=TEST_ACCOUNT, domain=1, truncate_response=False, include_unverified=False):
        with pytest.raises(AttributeError) as excinfo:
            # Will raise because the domain must be a string (specifically, six.text_type)
            pyHIBP.get_account_breaches(account=TEST_ACCOUNT, domain=1)
        assert "The domain parameter, if specified, must be a string" in str(excinfo.value)


class TestGetAllBreaches(object):
    def test_get_all_breaches(self):
        # def get_all_breaches(domain=None):
        resp = pyHIBP.get_all_breaches()
        assert isinstance(resp, list)
        assert len(resp) > 50
        assert isinstance(resp[0], dict)

    def test_get_all_breaches_filter_to_domain(self):
        # def get_all_breaches(domain=TEST_DOMAIN):
        resp = pyHIBP.get_all_breaches(domain=TEST_DOMAIN)
        assert isinstance(resp, list)
        # There can be multiple breaches in the system for a given domain
        assert len(resp) >= 1
        assert isinstance(resp[0], dict)
        assert resp[0]['Name'] == TEST_DOMAIN_NAME

    def test_get_all_breaches_false_if_domain_does_not_exist(self):
        resp = pyHIBP.get_all_breaches(domain=TEST_NONEXISTENT_ACCOUNT_NAME)
        assert not resp
        assert isinstance(resp, bool)

    def test_get_all_breaches_raise_if_not_string(self):
        # def get_all_breaches(domain=1):
        with pytest.raises(AttributeError) as excinfo:
            # Will raise because the domain must be a string (specifically, six.text_type)
            pyHIBP.get_all_breaches(domain=1)
        assert "The domain parameter, if specified, must be a string" in str(excinfo.value)


class TestGetSingleBreach(object):
    def test_get_single_breach(self):
        # pyHIBP.get_single_breach(breach_name=TEST_DOMAIN_NAME)
        resp = pyHIBP.get_single_breach(breach_name=TEST_DOMAIN_NAME)
        assert isinstance(resp, dict)
        assert resp['Name'] == TEST_DOMAIN_NAME

    def test_get_single_breach_when_breach_does_not_exist(self):
        # pyHIBP.get_single_breach(breach_name="ThisShouldNotExist")
        resp = pyHIBP.get_single_breach(breach_name="ThisShouldNotExist")
        # Boolean False will be returned from the above (as there is no breach named what we gave it).
        assert not resp

    def test_get_single_breach_raise_when_breach_name_not_specified(self):
        # pyHIBP.get_single_breach()
        with pytest.raises(AttributeError) as excinfo:
            # Will error because the breach_name must be specified
            pyHIBP.get_single_breach()
        assert "The breach_name must be specified, and be a string" in str(excinfo.value)

    def test_get_single_breach_raise_when_breach_name_is_not_a_string(self):
        # pyHIBP.get_single_breach(breach_name=1)
        with pytest.raises(AttributeError) as excinfo:
            # Will raise because the breach_name must be a string (specifically, six.text_type)
            pyHIBP.get_single_breach(breach_name=1)
        assert "The breach_name must be specified, and be a string" in str(excinfo.value)


class TestGetPastes(object):
    def test_get_pastes(self):
        # pyHIBP.get_pastes(email_address=TEST_ACCOUNT):
        resp = pyHIBP.get_pastes(email_address=TEST_ACCOUNT)
        # The return value is a list, containing multiple dicts (1 or more)
        assert isinstance(resp, list)
        for item in resp:
            assert isinstance(item, dict)

    def test_get_pastes_return_false_if_no_account(self):
        # pyHIBP.get_pastes(email_address=TEST_ACCOUNT):
        resp = pyHIBP.get_pastes(email_address=TEST_NONEXISTENT_ACCOUNT_NAME + "@example.invalid")
        assert not resp
        assert isinstance(resp, bool)

    def test_get_pastes_raise_if_email_not_specified(self):
        # pyHIBP.get_pastes():
        with pytest.raises(AttributeError) as excinfo:
            pyHIBP.get_pastes()
        assert "The email address supplied must be provided, and be a string" in str(excinfo.value)

    def test_get_pastes_raise_if_email_not_string(self):
        # pyHIBP.get_pastes(email_address=1):
        with pytest.raises(AttributeError) as excinfo:
            pyHIBP.get_pastes(email_address=1)
        assert "The email address supplied must be provided, and be a string" in str(excinfo.value)


class TestGetDataClasses(object):
    def test_get_data_classes(self):
        # get_data_classes():
        resp = pyHIBP.get_data_classes()
        assert isinstance(resp, list)
        assert len(resp) > 10
        assert "Passwords" in resp


class TestMiscellaneous(object):
    @pytest.mark.xfail(reason="The rate limit exists in the API docs, but responses are cached, and even attempting to manually (via browser) hit the limit isn't happening.")
    def test_raise_if_rate_limit_exceeded(self):
        """ The API will respond the same to all exceeded rate limits across all endpoints """
        # The rate limit exists, however all responses are cached; so we need to generate some random "accounts".
        import uuid
        rand_accts = ["{0}@test-suite.pyHIBP.example.com".format(str(uuid.uuid4())) for j in range(4)]

        with pytest.raises(RuntimeError) as excinfo:
            for item in rand_accts:
                pyHIBP.get_account_breaches(account=item, truncate_response=True)
        assert "HTTP 429" in str(excinfo.value)

    @pytest.mark.xfail(reason="The API does specify that no UA is supposed to generate a 403, but it doesn't seem to do so in a consistent manner anymore.")
    def test_raise_if_useragent_is_not_set(self, monkeypatch):
        # This should never be encountered normally, since we have the module-level variable/constant;
        # That said, test it, since we can, and since we might as well cover the line of code.
        headers = {'User-Agent': None}
        monkeypatch.setattr(pyHIBP, 'pyHIBP_HEADERS', headers)
        with pytest.raises(RuntimeError) as excinfo:
            pyHIBP.get_data_classes()
        assert "HTTP 403" in str(excinfo.value)

    def test_raise_if_invalid_format_submitted(self):
        # For example, if a null (0x00) character is submitted to an endpoint.
        with pytest.raises(RuntimeError) as execinfo:
            pyHIBP.get_account_breaches(account="\0")
        assert "HTTP 400" in str(execinfo.value)
