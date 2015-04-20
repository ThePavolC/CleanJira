import SOAPpy
import sys
from utils.files import FileUtils
from utils.run_check import check_argv
from properties import properties

def remove_schemes():
    username = None
    password = None
    server = None
    error_schemes = []

    file_utils = FileUtils()
    is_argv_ok, filename, is_test = check_argv(sys.argv)

    if is_argv_ok:
        pass
    else:
        return 0

    if is_test:
        username = properties['jira_test_username']
        password = properties['jira_test_password']
        server = properties['jira_test_server']
    else:
        username = properties['jira_live_username']
        password = properties['jira_live_password']
        server = properties['jira_live_server']

    data = file_utils.get_file_dic(filename)

    print 'Using server:', server

    soap = SOAPpy.WSDL.Proxy(server)
    auth = soap.login(username, password)

    print ''
    print 'Deleting Permission Schemes'

    total = len(data['NAME'])
    for scheme_name in data['NAME']:

        try:
            print ''
            print '%d/%d : %s' % (data['NAME'].index(scheme_name) + 1, total, scheme_name)
            soap.deletePermissionScheme(auth,scheme_name)
            print 'Scheme "%s" deleted' % scheme_name
        except Exception as e:
            print "ERROR: ",e
            print "ERROR witk scheme:", scheme_name
            error_schemes.append(scheme_name)

    print ''
    print 'Number of errors: %d' % len(error_schemes)
    print "Errors: ", error_schemes


if __name__ == '__main__':
    remove_schemes()
