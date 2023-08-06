import re

from . import install_requires, find


try:
    from collections import Optional
except ImportError:
    Optional = None


def increment_package_version(package_directory_or_setup_script=None):
    # type: (Optional[str]) -> None
    """
    Increment the version # of the referenced package
    """

    package_directory_or_setup_script = find.setup_script_path(package_directory_or_setup_script)

    with open(package_directory_or_setup_script) as setup_file:

        new_setup_file_contents = setup_file_contents = setup_file.read()

        for version_str in re.findall(
            r'\bversion\s*=\s*[\'"][^\'"]+[\'"]',
            setup_file_contents
        )[:1]:
            name_space = {}
            exec(version_str, name_space)
            dot_version_etc = re.split(r'([^\d.]+)', name_space['version'])
            if dot_version_etc:
                dot_version = dot_version_etc[0]
                etc = ''.join(dot_version_etc[1:])
                version_list = list(dot_version.split('.'))
                version_list[-1] = str(int(version_list[-1]) + 1)
                new_version = '.'.join(version_list) + etc
                new_setup_file_contents = setup_file_contents.replace(
                    version_str,
                    "version=%s" % repr(new_version),
                    count=1
                )

    updated = False  # type: bool

    if new_setup_file_contents != setup_file_contents:
        with open(package_directory_or_setup_script, 'w') as setup_file:
            setup_file.write(new_setup_file_contents)
        updated = True

    return updated
