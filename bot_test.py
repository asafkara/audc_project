import pytest
import requests

# import pytest-html
# --html=report1.html


bot_1 = {
    "id": 1,
    "name": "bot-1",
    "intents": []
}
bot_2 = {
    "id": 2,
    "name": "bot-2",
    "intents": []
}
bot_3 = {
    "id": 3,
    "name": "bot-3",
    "intents": []
}


def get_bots():
    return [bot_1, bot_2, bot_3]


class Bot:
    def __init__(self, id, name, intents: list):
        self.id = id
        self.name = name
        self.intents = intents

    def add_intents(self, intents):
        self.intents.append(intents)
        return self.intents


@pytest.mark.http_methods
def test_case_http_methods():
    bot1 = Bot(bot_1["id"], bot_1["name"], bot_1["intents"])
    bot1.add_intents("play_sound")
    data = {"name": bot1.name, "permission": "play_sound", "password": "password123"}
    r = requests.delete("http://localhost:8080/bot-1")
    assert r.status_code == 200
    r = requests.get("http://localhost:8080/bot-1")
    assert r.status_code == 200
    r = requests.post("http://localhost:8080/bot-1", json=data)
    assert r.status_code == 200
    r = requests.put("http://localhost:8080/bot-1", json=data)
    assert r.status_code == 200
    r = requests.patch("http://localhost:8080/bot-1", json=data)
    assert r.status_code == 200


@pytest.fixture
@pytest.mark.testbot1_put_response
def testbot1_put_response():
    bot1 = Bot(bot_1["id"], bot_1["name"], bot_1["intents"])
    bot1.add_intents("play_sound")
    data = {"name": bot1.name, "password": "password123", "intents": "play_sound"}
    response = requests.put("http://localhost:8080/bot-1", json=data)
    return response

# Test PUT, using Fixtures - Passed
@pytest.mark.testbot1_testcase1
def testbot1_testcase1(testbot1_put_response):
    assert testbot1_put_response.status_code == 200
    assert "User authenticated" in testbot1_put_response.text
    assert testbot1_put_response.headers["Content-Type"] == 'application/json'


#Test Failed
@pytest.mark.testbot1_testcase2
def testbot1_testcase2():
    bot1 = Bot(bot_1["id"], bot_1["name"], bot_1["intents"])
    bot1.add_intents("play_sound")
    data = {"name": bot1.name, "password": "password1243", "intents": "play_sound"} #Wrong password
    response = requests.patch("http://localhost:8080/bot-1", json=data)
    assert response.status_code == 200
    assert "User authenticated" in response.text #Wrong Content


@pytest.fixture
@pytest.mark.testbot2_post_response
def testbot2_post_response():
    bot2 = Bot(bot_2["id"], bot_2["name"], bot_2["intents"])
    bot2.add_intents("default_welcome_message")
    data = {"name": bot2.name, "intents": "default_welcome_message", "message": "this is a custom message!", "password": "password456"}
    response = requests.post("http://localhost:8080/bot-2", json=data)
    return response


# Test PUT, using Fixtures - Passed
@pytest.mark.testbot2_testcase1
def testbot2_testcase1(testbot2_post_response):
    assert testbot2_post_response.status_code == 200
    assert "User authenticated" in testbot2_post_response.text
    assert testbot2_post_response.headers["Content-Type"] == 'application/json'

# Test Passed
@pytest.mark.testbot2_testcase2
def testbot2_testcase2():
    bot2 = Bot(bot_2["id"], bot_2["name"], bot_2["intents"])
    bot2.add_intents("default_welcome_message")
    data = {"name": bot2.name, "intents": "default_welcome_message", "password": "password456"}
    response = requests.patch("http://localhost:8080/bot-2", json=data)
    assert "Hi this is the defualt welcome message" in response.text


@pytest.fixture
@pytest.mark.testbot3_patch_response
def testbot3_patch_response():
    bot3 = Bot(bot_3["id"], bot_3["name"], bot_3["intents"])
    data = {"name": bot3.name, "password": "password789"}
    response = requests.patch("http://localhost:8080/bot-3", json=data, headers={"Authorization": "Token 123456789"})


# Test PUT, using Fixtures - Passed
@pytest.mark.testbot3_testcase1
def testbot3_testcase1(testbot3_patch_response):
    assert "User authenticated" in testbot3_patch_response.text
    assert testbot3_patch_response.headers["Content-Type"] == 'application/json'

# Test Put, using wrong Token - Failed
@pytest.mark.testbot3_testcase2
def testbot3_testcase2():
    bot3 = Bot(bot_2["id"], bot_2["name"], bot_2["intents"])
    bot3.add_intents("intents")
    data = {"name": bot3.name, "password": "password456"}
    response = requests.put("http://localhost:8080/bot-3", json=data, headers={"Authorization": "Token 1234675589"})
    assert "Unauthenticated User" in response.text
    data = {"name": bot3.name, "password": "password456"}
    response = requests.put("http://localhost:8080/bot-3", json=data, headers={"Authorization": "Token 1234675589"})
    assert "Unauthenticated User" in response.text
    data = {"name": bot3.name, "password": "wrong"}
    response = requests.put("http://localhost:8080/bot-3", json=data, headers={"Authorization": "Token 1234675589"})
    assert "Unauthenticated User" in response.text
    data = {"name": bot3.name, "password": "password456"}
    response = requests.put("http://localhost:8080/bot-3", json=data, headers={"Authorization": "Token wrong"})
    assert "Unauthenticated User" in response.text
