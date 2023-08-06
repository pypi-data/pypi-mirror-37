import os

import re, pkg_resources

from . import find

try:
    from collections import Sequence, Optional
except ImportError:
    Sequence = Optional = None


def update_versions(package_directory_or_setup_script=None):
    # type: (Optional[str]) -> bool
    """
    Update setup.py installation requirements to (at minimum) require the version of each referenced package which is
    currently installed.

    Parameters:

        package_directory_or_setup_script (str):

            The directory containing the package. This directory must include a file named "setup.py".

    Returns:

         `True` if changes were made to setup.py, otherwise `False`
    """

    setup_script_path = find.setup_script_path(package_directory_or_setup_script)

    with open(setup_script_path) as setup_file:  # Read the current `setup.py` configuration

        setup_file_contents = setup_file.read()  # Retains the original setup file content for later comparison
        new_setup_file_contents = setup_file_contents  # This is the content which will be manipulated

        # Find the `install_requires` keyword argument
        for install_requires_str in re.findall(
            r'\binstall_requires\s*=\s*\[[^\]]*\]',
            setup_file_contents
        ):
            lines = install_requires_str.split('\n')  # type: Sequence[str]

            # Detect the indentation used for this parameter
            item_indentation = ''  # The indent for the parameter as a whole
            indentation = ''  # The indent for individual items
            if len(lines) > 1: # If there is only one line, the indentation is not relevant
                for line in lines:
                    match = re.match(r'^[ ]+', line)
                    if match:
                        group = match.group()
                        if group:
                            if item_indentation:
                                if len(group) > len(item_indentation):  # The first indent will be an item,
                                    item_indentation = group
                                elif len(group) < len(item_indentation):
                                    indentation = group
                            else:
                                indentation = item_indentation = group

            # Read the `install_requires` keyword and value into `namespace`
            name_space = {}
            exec(install_requires_str, name_space)
            install_requires = name_space['install_requires']

            # Create a string representation of the list defining updated installation requirements
            lines = ['install_requires=[']
            for requirement in install_requires:

                # Parse the requirement string
                parts = re.split(r'([<>=]+)', requirement)

                if len(parts) == 3:  # The requirement includes a version
                    referenced_package, operator, version = parts
                else:  # The requirement does not yet include a version
                    referenced_package = parts[0]
                    operator = '>='  # We assume the operator will be >= in the absence of an existing operator
                    version = '0'  # Ensures we use the package version found in the installed resource

                # Determine the package version currently installed for this resource
                try:
                    version = pkg_resources.get_distribution(referenced_package).version
                except pkg_resources.DistributionNotFound:
                    # If this package is not installed, it could be part of a project where references are handled
                    # by an IDE, so we look in sibling directories for a matching package.
                    requirement_setup_path = '../%s/setup.py' % referenced_package
                    try:
                        with open(requirement_setup_path) as requirement_setup_file:
                            requirement_setup_contents = requirement_setup_file.read()
                            for version_str in re.findall(
                                r'\bversion\s*=\s*[\'"][^\'"]+[\'"]',
                                requirement_setup_contents
                            ):
                                name_space = {}
                                exec(version_str, name_space)
                                version = name_space['version']
                                break
                    except FileNotFoundError:
                        pass
                lines.append("%s'%s'," % (item_indentation, referenced_package + operator + version))
            lines.append(indentation + ']')
            new_setup_file_contents = setup_file_contents.replace(
                install_requires_str,
                '\n'.join(lines)
            )

    updated = False  # type: bool

    if new_setup_file_contents != setup_file_contents:
        with open('./setup.py', 'w') as setup_file:
            setup_file.write(new_setup_file_contents)
            updated = True

    return updated
