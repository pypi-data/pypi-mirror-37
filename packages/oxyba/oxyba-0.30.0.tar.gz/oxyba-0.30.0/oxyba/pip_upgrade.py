
def pip_upgrade(v=1):
    import urllib3
    urllib3.disable_warnings()

    import pkg_resources
    from subprocess import PIPE, Popen
    import sys

    for dist in pkg_resources.working_set:
        if v >= 1:
            print("Try to upgrade package '" + dist.project_name + "'.")

        cmd = "pip install --upgrade " + dist.project_name
        p = Popen(cmd, shell=True, stdout=PIPE)

        if v >= 2:
            for msg in p.communicate():
                if msg is not None:
                    sys.stdout.write(msg)
            print("\n")

    if v >= 1:
        print("Upgrading finished")
