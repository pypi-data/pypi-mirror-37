from dalloriam.api import authentication

from tests.mocks.request import MockRequest

from unittest import mock

import pytest


def test_authorization_defaults_to_secret_if_no_key_provided():
    with mock.patch.object(authentication, 'request', MockRequest(headers={})):
        m = mock.MagicMock()
        authentication.authenticated('secret')(m)()
        m.assert_called_once()


def test_authorization_doesnt_call_internal_when_password_is_incorrect():
    with mock.patch.object(authentication, 'request', MockRequest(headers={'Authorization': 'Bad'})):
        m = mock.MagicMock()
        try:
            authentication.authenticated('good_password')(m)()
            pytest.raises('authenticated did not raise an exception on bad password!')  # pragma: nocover
        except ValueError:
            pass
