from datetime import datetime
import pytest
from mock import patch, Mock

from restapi import scheduler
from restapi.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@patch.object(scheduler, 'datetime', Mock(wraps=datetime))
def test_same_datetime(client, capsys):
    scheduler.datetime.now.return_value = datetime(2021, 4, 1, 13, 42)
    payload = {
        "content": "some content",
        "datetime": "2021-04-01 13:42"
    }

    responseOne = client.post("/scheduler/new", data=payload)
    responseTwo = client.post("/scheduler/new", data=payload)

    assert responseOne.status_code == 202
    assert responseTwo.status_code == 202
    captured = capsys.readouterr()
    output = captured.out
    assert output == "some content\nsome content\n"

@patch.object(scheduler, 'datetime', Mock(wraps=datetime))
def test_past_datetime(client, capsys):
    scheduler.datetime.now.return_value = datetime(2021, 4, 1, 12, 42)
    payload = {
        "content": "some content",
        "datetime": "2021-04-01 13:42"
    }

    responseOne = client.post("/scheduler/new", data=payload)
    responseTwo = client.post("/scheduler/new", data=payload)

    assert responseOne.status_code == 202
    assert responseTwo.status_code == 202
    captured = capsys.readouterr()
    output = captured.out
    assert output == ""

@patch.object(scheduler, 'datetime', Mock(wraps=datetime))
def test_different_datetime(client, capsys):
    scheduler.datetime.now.return_value = datetime(2021, 4, 1, 16, 00)
    payloadOne = {
        "content": "some content one",
        "datetime": "2021-04-01 16:00"
    }

    payloadTwo = {
        "content": "some content two",
        "datetime": "2021-04-01 16:01"
    }

    responseOne = client.post("/scheduler/new", data=payloadOne)
    responseTwo = client.post("/scheduler/new", data=payloadTwo)

    assert responseOne.status_code == 202
    assert responseTwo.status_code == 202
    captured = capsys.readouterr()
    output = captured.out
    assert output == "some content one\n"


def test_invalid_datetime(client, capsys):
    payloadErr = {
        "content": "some content one",
        "datetime": "x"
    }

    responseOne = client.post("/scheduler/new", data=payloadErr)

    assert responseOne.status_code == 400
    responseJson = responseOne.get_data(as_text=True)
    assert responseJson == "{\"message\": {\"datetime\": \"time data 'x' does not match format '%Y-%m-%d %H:%M'\"}}\n"
