import requests
import json
import os

from . import util
from . import constants

##########################################################################################

def fn_register_service(withToken, serviceData) :

    authHeaders = {
        'Contetn-Type': 'application/json',
        'x-access-token': withToken
    }
    response = requests.post(url=constants.URL_MYSERVICE, headers=authHeaders, json=serviceData)

    if response.status_code == 200:
        jsonResponse = util.fn_get_json_from(response)
    else :
        print(response)


##########################################################################################
def fn_load_osifservice_json():

    try:
        serviceProfilePath = os.path.join('.', constants.OSIF_SERVICE_PROFILE_NAME)
        print('Load OSIF Service description: ', serviceProfilePath )


        with open(serviceProfilePath) as f:
            data = json.load(f)

        return data['service']

    except Exception as e:
        print('Fail to load "', constants.OSIF_SERVICE_PROFILE_NAME, '" file')
        return None
