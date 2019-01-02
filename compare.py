import argparse
import sys

import functions

try:
    import colorama

    colorama.init()
except ImportError:
    pass


def main():
    # check path first
    if not functions.check_in_path("choco"):
        functions.print_error(
            "Chocolatey needs to be installed and in the system PATH."
        )
        sys.exit(1)

    # check if admin
    if not functions.check_admin():
        functions.print_error(
            "You need to run this program as an administrator to export Windows features"
        )
        sys.exit(1)

    # arguments
    parser = argparse.ArgumentParser(
        description="Windows feature comparison tool for Chocolately"
    )
    parser.add_argument("input_file", help="input package file to compare")
    parser.add_argument(
        "-o",
        "--output",
        help="path to windows features output file (default: %(default)s)",
        default="windows_features_new.config",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="output more detailed messages (default: %(default)s)",
        action="store_true",
    )

    args = parser.parse_args()

    if args.verbose:
        functions.print_info("Getting enabled Windows features")

    # raw output from command
    windows_string = functions.get_command_output(
        ["choco", "list", "--source", "windowsfeatures"]
    )

    if args.verbose:
        functions.print_info("Windows features packages retrieved")

    # convert raw string to a list of packages
    installed_windows_list = functions.windows_packages_string_to_list(windows_string)

    if args.verbose:
        functions.print_info("Getting Windows features from " + args.input_file)

    # get a list of packages from the given xml file
    xml_windows_list = functions.windows_packages_xml_to_list(args.input_file)

    # get items that are in the xml file, but not enabled
    desired_windows_list = [
        item for item in installed_windows_list if item not in xml_windows_list
    ]

    if not desired_windows_list:
        functions.print_info(
            "No Windows features in export list that are not already enabled"
        )
        sys.exit(0)

    if args.verbose:
        functions.print_info("Disabled Windows features to be exported:")
        for i in desired_windows_list:
            functions.print_info(str(i))
        functions.print_info("Creating Windows features XML file")

    # convert list to XML file
    functions.create_xml(desired_windows_list, args.output)
    functions.print_info("Windows features XML file created at: " + args.output)


if __name__ == "__main__":
    main()
