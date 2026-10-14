import pytest

from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.storage.fallback import FallbackStorage

@pytest.fixture
def authenticated_request_factory():
    def make_request(user):
        request = RequestFactory().get("/")

        session_middleware = SessionMiddleware(lambda request: None)
        session_middleware.process_request(request)
        request.session.save()

        request._messages = FallbackStorage(request)
        request.user = user

        return request

    return make_request