import requests
import json

from ddlcli.utils import TokenAuth

def login_user(data, master_endpoint):
    login_request = requests.post("{}/api/v1/user/login/".format(master_endpoint), data=data)
    login_response = json.loads(login_request.text)

    if not login_request.ok:
        if login_request.status_code == 401:
            raise Exception("You need to register before login")
        else:
            raise Exception("Error: {}".format(login_response.get("error")))

    auth_token = login_response.get('auth_token', None)
    return TokenAuth(auth_token), login_response

def register_user(master_endpoint):
    email = input("Please enter your email address: ")
    password = input("Please enter your password: ")
    re_password = input("Please re-enter your password: ")

    if password != re_password:
        raise Exception("your passwords do not match")

    data = {
        'email': email,
        'password': password
    }

    r = requests.post("{}/api/v1/user/register/".format(master_endpoint), data=data)
    print("Status: {}".format(r.status_code))
    resp = json.loads(r.text)
    if r.ok == False:
        raise Exception("Error: {}".format(resp.get("error")))
    else:
        print("Registered successfully")
