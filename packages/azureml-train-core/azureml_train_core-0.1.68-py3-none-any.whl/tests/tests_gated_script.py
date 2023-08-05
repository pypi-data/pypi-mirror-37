from os import path
import sys

from base_e2e import BaseE2E


def run_tests(filelist):
    for f in filelist:
        print("Running " + f)
        cmd = ["python", f]
        framework.utils.run_command(cmd)
        print("Done")


if __name__ == '__main__':
    curdir = path.dirname(path.abspath(__file__))
    sys.path.append(path.join(curdir, "../../../tests"))

    import framework.utils

    filelist = framework.utils.get_test_files(curdir)

    if len(sys.argv) > 1:
        # unit-test only build definition will pass this arg
        if sys.argv[1].lower() == 'unit-tests-only':
            print('Flag unit-tests-only is provided in the commandline. Limiting to unit tests')
            # uses file name convention to pick unit tests
            filelist = list(filter(lambda file: 'unittests' in file, filelist))
    else:
        BaseE2E._az_login()

    run_tests(filelist)
