class FileUtils(object):

    def _get_file_lines(self,filename):
        """Reads file and returns each line in list"""
        file_lines = []

        with open(filename,'r') as opened_file:
            for line in opened_file:
                file_lines.append(line)

        return file_lines

    def get_file_dic(self,filename):
        """Creates dictionary from table data.

        Name of column is key in dictionary and column data are
        value in dictionary represented as list.
        """
        file_lines = self._get_file_lines(filename)

        data = {}
        header_list = []

        for idx,line in enumerate(file_lines):

            if idx == 0:
                continue

            if idx == 1:
                headers = line.split('|')
                for header in headers:
                    header = header.strip()
                    header_list.append(header)
                    data[header] = []
                continue

            values = line.split('|')

            for i,value in enumerate(values):
                value = value.strip()

                data[header_list[i]].append(value)

        if data.has_key(''):
            data.pop('')

        return data

    def print_file_dic(self, filename):
        """Print file dictionary in nicer form"""
        data = self.get_file_dic(filename)

        first_key = data.keys()[0]
        first_value = data[first_key]
        number_of_lines = len(first_value)

        for header in data.keys():
            print header, '\t',
        print ''

        for line in xrange(number_of_lines):
            for header in data.keys():
                print data[header][line] + "\t",
            print ""

if __name__ == "__main__":
    pass
