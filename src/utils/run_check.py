def check_argv(argv):
    python_file_name = argv[0]
    usage_msg = "Usage: python %s [-test | -live] filename.txt" % python_file_name
    is_test = True

    if len(argv) > 1:
        if '-test' in argv:
            is_test = True
        elif '-live' in argv:
            is_test = False
        else:
            print usage_msg
            return (False, None, is_test)

        if len(argv) < 3:
            print usage_msg
            return (False, None, is_test)
        else:
            filename = argv[2]
            return (True, filename, is_test)
    else:
        print usage_msg
        return (False, None, is_test)
