"""
Usefull function needed by the module.
"""

import os
import socket

from datetime import date
from importlib import import_module
from pathlib import Path


def which(program):
    """
    Fetch for the absolute path of a binary, same as `which` Unix command.

    :param program: Name of the program
    :type program: str
    :return: Absolute path of the program, or None if path not found.
    :rtype: str

    :Example:

    >>> which("ls")
    /bin/ls
    """

    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, _ = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def hostname():
    """
    Return the hostname of the current machine.

    :return: the hostname of the current machine
    :rtype: str
    """
    if socket.gethostname().find(".") >= 0:
        return socket.gethostname()
    else:
        return socket.gethostbyaddr(socket.gethostname())[0]


def render(template):
    """
    Format the template using hostname variable and date of the day.

    :param template: string to format
    :param template: string to format

    :return: the rendered template
    :rtype: str

    :Example:
    >>> render("machine-{hostname}-{date}")
    """
    return template.format(hostname=hostname(), date=date.today())


def factory(class_name="", from_={}):
    """
    Return class object depending the name.

    :param class_name: ID of the Task, not case sensitive.
    :param from_: Dict with str name as key and Class as value.
    :type class_name: str
    :type from_: dict
    """
    return from_[class_name.lower()]


def load(path=".", pkg="", suffix="Task"):
    """
    Dynamicaly create a list of all class from a module.

    :param path: Module directory or a file in the module directory.
    :param pkg: Absolute name of the module.
    :param suffix: String part in the name of each class to load.

    :type path: str
    :type pkg: str
    :type suffix: str

    :return: Dictionary of all class loaded.
             With as key a string containing the class name in lowercase and without the suffix part.
             And as value the class (not the object, need to be instantiate)
    :rtype: dict
    """
    pwd = Path(path).resolve()
    if pwd.is_file():
        pwd = pwd.parent
    tasks = {}
    for f in pwd.glob("*{}.py".format(suffix.capitalize())):
        class_name = Path(f).stem
        slug_name = class_name.lower().replace(suffix.lower(), "")
        module = import_module("." + class_name, package=pkg)
        tasks[slug_name] = getattr(module, class_name)
    return tasks
