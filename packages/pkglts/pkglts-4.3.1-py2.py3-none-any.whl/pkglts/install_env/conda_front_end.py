"""Conda front end to install package in current environment.
"""
from json import loads
from subprocess import Popen, PIPE


def installed_packages():
    """Iterate on all packages installed in the current python environment.

    return:
        (iter of str)
    """
    process = Popen(["conda", "list", "--json"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, _ = process.communicate("")
    if process.returncode != 0:
        raise UserWarning("unable to execute 'conda list'")

    for pkg in loads(output):
        yield pkg.split("-")[0]


def install(name):
    """Install a package in the current python environment.

    arg:
     - name (str): name of the package

    return:
     - (bool): whether installation was successful or not
    """
    process = Popen(["conda", "install", name], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    process.communicate("")

    if process.returncode == 0:
        return True

    # try to use pip if conda install fail
    from .pip_front_end import install as pip_install
    return pip_install(name)
