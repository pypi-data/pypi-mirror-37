#!/usr/bin/env python
# coding=utf-8



##########################################################################################
import optparse
import sys

from . import util
from . import constants
from . import service
from . import login
from . import dockertool

##########################################################################################

def usage(msg=None):
    """
    usage for this search program
    :param msg:
    :return:
    """
    if msg:
        sys.stderr.write('%s\n' % msg)
    print('''
usage: {0} [options] query_string
  query and search result from CVE
  options are:
    -h, --help : show this message
    -s, --show_hidden : show hidden directory
'''.format(sys.argv[0]))
    sys.exit(1)


def __versionCode(versionCode):
    return "%d.%d.%d" % (versionCode['major'], versionCode['minor'], versionCode['revision'])

##########################################################################################
def main():

    try:

        usage = "Usage: %prog [options]"
        p = optparse.OptionParser(usage=usage, version="%prog 1.0.0")
        options, arguments = p.parse_args()

        # make version neutral env.
        #   1. input(v3.x) and raw_input(2.x)
        util.fn_python_modernize()

        # check execution environment
        #   1. docker command available
        #   2. osif.json file is exists
        if util.fn_check_environment() == False:
            exit(-1)

        serviceMetadata = service.fn_load_osifservice_json()
        if serviceMetadata == None:
            print('[ERROR] Fail to load OSIF Service file(', constants.OSIF_SERVICE_PROFILE_NAME , ')')
            exit(-1)

        print('     Service name: ', serviceMetadata['serviceName'])
        print('          Version: ', __versionCode(serviceMetadata['versionCode']))
        print('      Description: ', serviceMetadata['serviceDesc'])

        dockertool.fn_build()

        login_try_count = 0
        while login_try_count < 4:
            login_try_count += 1
            token = login.fn_login()
            #token = login.fn_login_fake()

            if token == '' :
                continue
            else :
                break

        if token == '' :
            print('[ERROR] Exit tool: failed to login')
            exit(-1)

        service.fn_register_service(withToken=token, serviceData=serviceMetadata)

    except Exception as e:
        usage(str(e))


##########################################################################################


if __name__ == '__main__':
    main()
