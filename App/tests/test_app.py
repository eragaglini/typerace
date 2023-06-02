from App.main import create_app
from App.events import rooms, get_room_by_name
import pytest
from flask import request, url_for

# run tests with: pytest path-to-test-folder -W ignore::DeprecationWarning


@pytest.fixture(scope="module")
def app():
    app = create_app()
    app.config["WTF_CSRF_ENABLED"] = False
    return app


@pytest.fixture(scope="module")
def client(app):
    return app.test_client()


def test_index_route(client):
    with client:
        response = client.get("/")
        assert response.status_code == 200
        response = client.post("/")
        assert response.status_code == 405


def test_create_room(client):
    with client:
        response = client.get("/create-room")
        assert response.status_code == 200
        formdata = {
            "name": "testuser",
            "room": "testroom",
        }
        response = client.post("/create-room", data=formdata, follow_redirects=True)
        assert response.status_code == 200
        # Check that there was one redirect response.
        assert len(response.history) == 1
        assert response.request.path == url_for(".chat")
        assert len(rooms) == 1
        assert get_room_by_name("testroom") is not None
