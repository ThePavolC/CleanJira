import SOAPpy
import sys

class Main(object):

    def __init__(self):
        self.args = sys.argv[1:]

    def get_file(self,filename):
        """Get file object"""
        ff = []
        with open(filename,'r') as f:
            for line in f:
                ff.append(line)
        return ff

    def get_file_dic(self,filename):
        """Transform file content to dictionary"""
        f = self.get_file(filename)

        data = {}
        hh = []
        for idx,line in enumerate(f):
            if idx == 0:
                header = line.split('|')
                for h in header:
                    h = h.strip()
                    hh.append(h)
                    data[h] = []
                continue

            values = line.split('|')
            for i,v in enumerate(values):
                v = v.strip()
                data[hh[i]].append(v)
        return data

    def print_file_dic(self,data):
        """Print file dictionary in nice form"""
        max_i = len(data['id'])
        print max_i
        for i in range(0,max_i):
            output = ""
            for k in data:
                output = output + " : " + data[k][i] + " (" + k + ")"
            print output

def main():

    main = Main()

    test = True
    filename = ""
    if len(main.args) > 0:
        if '-test' in main.args:
            test = True
        if '-live' in main.args:
            test = False
        if len(main.args) < 2:
            print "usage: python main.py [-test | -live] filename.txt"
            return
        else:
            filename = main.args[1]
    else:
        print "usage: python main.py [-test | -live] filename.txt"
        return

    soap_live = 'http://live.jira.server.com/rpc/soap/jirasoapservice-v2?wsdl'
    soap_test = 'http://test.jira.server.com/rpc/soap/jirasoapservice-v2?wsdl'
    soap_server = soap_test
    if test:
        user = 'admin'
        pas = 'password'
        soap_server = soap_test
    else:
        user = 'admin'
        pas = 'password'
        soap_server = soap_live

    data = main.get_file_dic(filename)

    print "Using server:",soap_server

    soap = SOAPpy.WSDL.Proxy(soap_server)
    auth = soap.login(user, pas)

    print "Connected"
    print "Deleting Empty Groups"

    errors = []
    not_delete = []
    total = len(data['group_name'])
    for g in data['group_name']:
        try:
            print ""
            print str(data['group_name'].index(g) + 1) + "/" + str(total)
            group = soap.getGroup(auth,g)
            g_name = group.name
            users = group.users
            num_users = len(users)
            if g_name.startswith("special_group"):
                print "  Will not be deleted:",str(g_name)
                not_delete.append(g_name)
            else:
                print "Delete group: '", str(g_name),"', users:",num_users
                soap.deleteGroup(auth,g_name,'jira-users')
                print "Group: '", str(g_name),"' deleted"
        except Exception as e:
            print "ERROR: ",e
            print "ERROR with group:", g
            errors.append(g)

    print ""
    print 10 * "*"
    print ""

    print "Number of errors: ", len(errors)
    print "Errors: ",errors

    print ""
    print 10 * "*"
    print ""

    print "Number of not deleted groups: ", len(not_delete)
    print "Not deleted groups: ",not_delete

if __name__ == '__main__':
    main()
