import SOAPpy
import sys
from utils.files import FileUtils
from utils.run_check import check_argv
from properties import properties

def remove_projects():
    username = None
    password = None
    server = None
    error_projects = []

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
    print 'Deleting projects'

    for project_key in data['Project Key']:
        try:
            jira_project = soap.getProjectByKey(auth,project_key)
            print ''
            print 'Key: %s Name: %s Lead: %s' % (jira_project.key, jira_project.name, jira_project.lead)
            try:
                soap.deleteProject(auth,jira_project.key)
                print 'Project: "%s" deleted.' % jira_project.name
            except Exception as e:
                print "ERROR: ",e
                print "ERROR deleting project ", project_key
        except Exception as e:
            print "ERROR: ",e
            print "ERROR witk key", project_key
            error_projects.append(project_key)
        print ""

    print ''
    print 'Number of errors: %d' % len(error_projects)
    print 'Errors: ', error_projects


if __name__ == '__main__':
    remove_projects()
