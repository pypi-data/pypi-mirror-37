from urllib.parse import urlparse
from codegenhelper import debug
import requests
import urllib
import demjson
from getpass import getpass
def get_input(name):
    result = input("please input {}:".format(name))
    if not result:
        raise Exception("no {} is supplied".format(name))
    return result

def get_login_url(url):
    return (lambda result:"{scheme}://{netloc}/auth/login".format(scheme = debug(result, "result").scheme, netloc = result.netloc))(urlparse(url))

def getToken(login_url, name, pwd):
    return (lambda result:\
            result.content.decode(result.encoding))\
            (requests.post(login_url, json={"name": name, "pwd": pwd}))

def get_json(url, name, token):
    return debug(requests.get(url, headers={"name": name, "token": token}).text, "get_json_result")

def getJson(url, userName=None, password=None):
    return demjson.decode(\
                          (lambda name, pwd:\
            get_json(url, name, getToken(get_login_url(url), name, pwd))) \
            (userName or get_input("username"), password or getpass("please input password:")) \
    )
