from urllib.error import HTTPError

import requests
import json

"""
API_endpoint_testing

Functions
----------
test_get_user : GET
    test if user gets retrieved
test_send_message : POST
    test if data gets inserted into system
test_signup : POST
    test if data gets inserted into system
test_get_all_friends : GET
    test if friends gets retrieved
test_get_chat_rooms : GET
    test if rooms gets retrieved
test_get_chat_history : GET
    test if chat history of particular room gets retrieved

"""


def test_get_user():
    """
    Test for user retrieval

    Endpoint
    ----------
    url: /api/profile/<ID>/

    Return
    -------
    - user details of id 3
    """
    try:
        print("Running GET User data")
        request = requests.get('http://127.0.0.1:8080/api/profile/4/')
        if (request.status_code == 200):
            data = json.loads(request.text)
            if (data['user_id']):
                print("Get User data Passed")
                return True
            else:
                raise ValueError("Test length different from database")
        else:
            raise HTTPError('http://127.0.0.1:8080/api/chat/3/4/', request.status_code, "API not available", "Connection Issues", None)
    except Exception as error:
        return error


def test_send_message():
    """
    Test for posting message

    Endpoint
    ----------
    url: /api/chat/message/

    Return
    -------
    - HTTP Response Status 200
    """
    try:
        print("Running POST send message")
        request = requests.get('http://127.0.0.1:8080/api/chat/message/')
        if (request.status_code == 200):
            print("Create Message Passed")
        else:
            raise HTTPError('http://127.0.0.1:8080/api/chat/3/4/', request.status_code, "API not available", "Connection Issues", None)
    except Exception as error:
        return error


def test_signup():
    """
    Test for signup retrieval

    Endpoint
    ----------
    url: /api/signup/

    Return
    -------
    - A user account details of recently registered user
    """
    request = requests.get('http://127.0.0.1:8080/api/signup')
    try:
        print("Running POST signup")
        if request.status_code == 200:
            result = json.loads(request.text)
            if result["username"] == "johncheng":
                print("Create user has passed the test")
            else:
                raise AttributeError("No username johncheng")
        else:
            raise HTTPError('http://127.0.0.1:8080/api/signup', request.status_code, request.text, "Connection Issues", None)
    except Exception as error:
        return error


def test_get_all_friends():
    """
    Test for friends retrieval

    Endpoint
    ----------
    url: /api/friends/3/

    Return
    -------
    - all friends of id 3 user
    """
    try:
        print("Running GET All Friends")
        request = requests.get('http://127.0.0.1:8080/api/friends/3/')
        if (request.status_code == 200):
            result = json.loads(request.text)
            if (len(result) == 3):
                print("Get All Friends Passed")
                return True
            else:
                raise ValueError("Test length different from database")
        else:
            raise HTTPError('http://127.0.0.1:8080/api/chat/3/4/', request.status_code, "API not available", "Connection Issues", None)
    except Exception as error:
        return error


def test_get_chat_rooms():
    """
    Test for rooms retrieval for a particular user

        Endpoint
        ----------
        url: /api/user/rooms/3/

        Return
        -------
        - all created and joined rooms of id 3 user
        """
    try:
        print("Running GET Chat Room")
        request = requests.get('http://127.0.0.1:8080/api/user/rooms/3/')
        if (request.status_code == 200):
            result = json.loads(request.text)
            if (len(result) == 3):
                print("Get Chat Room Passed")
                return True
            else:
                raise ValueError("Test length different from database")
        else:
            raise HTTPError('http://127.0.0.1:8080/api/chat/3/4/', request.status_code, "API not available", "Connection Issues", None)
    except Exception as error:
        return error


def test_get_chat_history():
    """
    Test for chat history retrieval for a particular user

        Endpoint
        ----------
        url: /api/chat/<str:user_id>/<str:room_id>

        Return
        -------
        - all created and joined rooms of id 3 user
        """
    try:
        print("Running GET Chat history")
        request = requests.get('http://127.0.0.1:8080/api/chat/3/4/')
        if (request.status_code == 200):
            result = json.loads(request.text)
            if (len(result) > 5):
                print("Get Chat History Passed")
                return True
            else:
                raise ValueError("Test length different from database")
        else:
            raise HTTPError('http://127.0.0.1:8080/api/chat/3/4/', request.status_code, "API not available", "Connection Issues", None)
    except Exception as error:
        return error


if __name__ == "__main__":
    response_get_chat = test_get_chat_history()
    print(response_get_chat)
    response_create_signup = test_signup()
    print(response_create_signup)
    response_get_chat = test_get_chat_rooms()
    print(response_get_chat)
    response_send_message = test_send_message()
    print(response_send_message)
    response_get_user = test_get_user()
    print(response_get_user)
    response_get_all_friends = test_get_all_friends()
    print(response_get_all_friends)
