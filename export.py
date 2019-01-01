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

    # arguments
    parser = argparse.ArgumentParser(
        description="Package list exporter for Chocolately"
    )
    parser.add_argument(
        "-dl",
        "--disable-local",
        help="disables exporting a list of locally installed packages (default: %(default)s)",
        action="store_true",
    )
    parser.add_argument(
        "-lo",
        "--local-output",
        help="path to locally installed packages output file (default: %(default)s)",
        default="local_packages.config",
    )
    parser.add_argument(
        "-p",
        "--preserve-versions",
        help="save the versions of the locally installed packages (default: %(default)s)",
        action="store_true",
    )
    parser.add_argument(
        "-w",
        "--windows-features",
        help="export a list of enabled Windows features. Program needs to be run with Administrator privileges in order for this to work (default: %(default)s)",
        action="store_true",
    )
    parser.add_argument(
        "-wo",
        "--windows-output",
        help="path to windows features output file (default: %(default)s)",
        default="windows_features.config",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="output more detailed messages (default: %(default)s)",
        action="store_true",
    )

    args = parser.parse_args()

    if not args.disable_local:
        if args.verbose:
            functions.print_info("Getting locally installed packages")

        # raw output from command
        local_string = functions.get_command_output(["choco", "list", "--local-only"])

        if args.verbose:
            functions.print_info("Locally installed packages retrieved")

        # convert raw string to a list of packages
        local_list = functions.local_packages_string_to_list(
            local_string, args.preserve_versions
        )

        if args.verbose:
            functions.print_info("Creating locally installed packages XML file")

        # convert list to XML file
        functions.create_xml(local_list, args.local_output)
        functions.print_info(
            "Locally installed packages XML file created at: " + args.local_output
        )

    if args.windows_features:
        # check if admin
        if not functions.check_admin():
            functions.print_error(
                "You need to run this program as an administrator to export Windows features"
            )
            sys.exit(1)

        if args.verbose:
            functions.print_info("Getting enabled Windows features")

        # raw output from command
        windows_string = functions.get_command_output(
            ["choco", "list", "--source", "windowsfeatures"]
        )

        if args.verbose:
            functions.print_info("Enabled Windows features retrieved")

        # convert raw string to a list of packages
        windows_list = functions.windows_packages_string_to_list(windows_string)

        if args.verbose:
            functions.print_info("Creating Windows features XML file")

        # convert list to XML file
        functions.create_xml(windows_list, args.windows_output)
        functions.print_info(
            "Windows features XML file created at: " + args.windows_output
        )


if __name__ == "__main__":
    main()
