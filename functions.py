import ctypes
import re
import shutil
import subprocess
import sys

# import colorama if available
try:
    import colorama

    COLOR = True
except ImportError:
    COLOR = False

# try to preferably import the c implementation of ElementTree
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def check_in_path(name):
    """Checks if given name exists in the system PATH"""
    return bool(shutil.which(name))


def check_admin():
    """Checks if program has admin privledges on Windows"""
    return ctypes.windll.shell32.IsUserAnAdmin() == 1


def print_info(message):
    """Prints info message to stdout"""
    if COLOR:
        print(colorama.Fore.BLUE + "INFO" + colorama.Style.RESET_ALL + "  | " + message)
    else:
        print("INFO  | " + message)


def print_error(message):
    """Prints error message to stderr"""
    if COLOR:
        print(
            colorama.Fore.RED
            + "ERROR"
            + colorama.Style.RESET_ALL
            + " | "
            + colorama.Fore.RED
            + message
            + colorama.Style.RESET_ALL,
            file=sys.stderr,
        )
    else:
        print("ERROR | " + message, file=sys.stderr)


def get_command_output(command):
    """Returns output from a command passed as a list"""
    try:
        output_string = subprocess.check_output(command).decode("utf-8")
    except subprocess.CalledProcessError as e:
        print(e.output.decode("utf-8"))
        sys.exit(1)

    return output_string


def local_packages_string_to_list(package_string, preserve_versions):
    """Converts string of packages to list of dictionaries"""
    packages = []

    # removes trailing whitespace
    package_string = package_string.rstrip()
    # regex match
    matches = re.findall(r"\S+ [\d|\.]+", package_string)

    # splits each string and adds it to the dict
    for match in matches:
        [package, version] = match.split()
        tmp = {"id": package}
        # add version if requested
        if preserve_versions:
            tmp["version"] = version
        packages.append(tmp)

    return packages


def windows_packages_string_to_list(package_string):
    """Converts string of packages to list of dictionaries"""
    packages = []

    # removes trailing whitespace
    package_string = package_string.rstrip()
    # regex match
    matches = re.findall(r"\S+\s+\| Enabled", package_string)

    # splits each string and adds it to the dict
    for match in matches:
        package = match.split()[0]
        tmp = {"id": package}
        packages.append(tmp)

    return packages


def windows_packages_xml_to_list(filename):
    """Converts xml file to a list of package dictionaries"""
    packages = []

    # parse
    tree = ET.parse(filename)
    # get root tag
    root = tree.getroot()
    # iterate through children
    for package in root:
        packages.append(package.attrib)

    return packages


def create_xml(package_list, filename):
    """Creates xml file from the package list"""

    # create the root tag
    packages = ET.Element("packages")
    # create child elements
    for package in package_list:
        ET.SubElement(packages, "package", package)

    # create a new XML file with the tree
    xmlstring = ET.tostring(packages).decode("utf-8")
    with open(filename, "w") as outfile:
        outfile.write(xmlstring)
