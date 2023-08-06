#!/usr/bin/env python

# coding=utf-8


##########################################################################################
import requests
import getpass

from . import constants
from . import util

##########################################################################################


defaultHeaders = {'Contetn-Type': 'application/json'}

##########################################################################################
def fn_login():
    try:
        util.fn_python_modernize()

        userid = input('OSIF Portal login:')
        password = getpass.getpass(     'Password:')

        loginData = {'userid': userid, 'password': password}

        response = requests.post(url=constants.URL_LOGIN, headers=defaultHeaders, data=loginData)

        if response.status_code == 200:
            jsonResponse = util.fn_get_json_from(response)
            return jsonResponse['token']
        else:
            jsonResponse = util.fn_get_json_from(response)
            print('Login failed: ' + jsonResponse['message'])
            return ''

    except Exception as e:
        print('Login failed: ', e)
        return ''


def fn_login_fake():
    try:
        util.fn_python_modernize()

        userid = 'user00038@acme.re.kr'
        password = 'user1234%^&*'

        loginData = {'userid': userid, 'password': password}

        response = requests.post(url=constants.URL_LOGIN, headers=defaultHeaders, data=loginData)

        if response.status_code == 200:
            jsonResponse = util.fn_get_json_from(response)
            return jsonResponse['token']
        else:
            jsonResponse = util.fn_get_json_from(response)
            print('Login failed: ' + jsonResponse['message'])
            return ''

    except Exception as e:
        print('Login failed: ', e)
        return ''