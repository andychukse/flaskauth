import pytest
# from app.main import hello_message


def test_hello_message():
	response = client.get('/hello')
	assert response.status_code == 200
    assert b"Hello It Works" in response.data