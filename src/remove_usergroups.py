import SOAPpy
import sys
from utils.files import FileUtils
from utils.run_check import check_argv
from properties import properties

def remove_usergroups():
    username = None
    password = None
    server = None
    keep_group = properties['remove_usergroup']['keep_group']
    error_groups = []
    not_deleted_groups = []

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
    print 'Deleting Empty Groups'


    total = len(data['group_name'])

    for group_name in data['group_name']:
        print ''
        print '%d/%d : ' % (data['group_name'].index(group_name) + 1, total),
        print group_name

        try:
            jira_group = soap.getGroup(auth,group_name)
            jira_group_name = jira_group.name
            jira_group_users = jira_group.users
            num_users = len(jira_group.users)

            if jira_group_name.startswith(keep_group):
                print '* Will not be deleted: %s' % str(jira_group_name)
                not_deleted_groups.append(jira_group_name)
            else:
                print ('Delete group "%s" with %d users.' %
                    (jira_group_name, num_users))

                soap.deleteGroup(auth,jira_group_name,'jira-users')

                print 'Group "%s" deleted.' % jira_group_name
        except Exception as e:
            print "ERROR: ",e
            print "ERROR with group:", group_name
            error_groups.append(group_name)

    print ""
    print 10 * "*"
    print "Number of errors: ", len(error_groups)
    print "Errors: ",error_groups
    print 10 * "*"
    print ""

    print "Number of not deleted groups: ", len(not_deleted_groups)
    print "Not deleted groups: ",not_deleted_groups

if __name__ == '__main__':
    remove_usergroups()
