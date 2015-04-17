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
        max_i = len(data['ID'])
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
    print "Deleting Permission Schemes"

    errors = []
    total = len(data['NAME'])
    for s in data['NAME']:
        try:
            print str(data['NAME'].index(s) + 1) + "/" + str(total), "> Scheme Name:", s
            soap.deletePermissionScheme(auth,s)
            print "Scheme '",s,"' deleted"
        except Exception as e:
            print "ERROR: ",e
            print "ERROR witk scheme:", s
            errors.append(s)

    print "Number of errors: ", len(errors)
    print "Errors: ",errors


if __name__ == '__main__':
    main()
