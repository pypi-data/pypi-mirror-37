# Copyright 2018 Graham Binns <graham@outcoded.uk>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""A static-analysis Python import guardian.

Prevents your code from importing things it shouldn't to places that it
oughtn't.
"""

from argparse import ArgumentParser
import glob
import json
import os
import re
import sys
from textwrap import dedent


FORBIDDEN_FROM_WILDCARD = "*"

# To search for escaped newline chars.
ESCAPED_NL_REGEX = re.compile("\\\\\n", re.M)
IMPORT_REGEX = re.compile("^\s*import +(?P<module>.+)$", re.M)
FROM_IMPORT_SINGLE_REGEX = re.compile(
    "^\s*from (?P<module>.+) +import +"
    "(?P<objects>[*]|[a-zA-Z0-9_, ]+)"
    "(?P<comment>#.*)?$", re.M)
FROM_IMPORT_MULTI_REGEX = re.compile(
    "^\s*from +(?P<module>.+) +import *[(](?P<objects>[a-zA-Z0-9_, \n]+)[)]$",
    re.M)
SPLIT_REGEX = re.compile(",\s*")


def find_imports(file_contents):
    """Find all the imports within a file and return them as a dict."""
    imports = {}

    # First, find any simple "import..." statements.
    position = 0
    while True:
        match = IMPORT_REGEX.search(file_contents, position)
        if match is None:
            break
        # These imports are marked by a "None" value.
        # Multiple modules in one statement are split up.
        for module in SPLIT_REGEX.split(match.group("module").strip()):
            imports[module] = set()
        position = match.end()

    # Now find any "from ... import" statements.
    for pattern in (FROM_IMPORT_SINGLE_REGEX, FROM_IMPORT_MULTI_REGEX):
        position = 0
        while True:
            match = pattern.search(file_contents, position)
            if match is None:
                break
            import_objects = SPLIT_REGEX.split(
                match.group("objects").strip(" \n,"))
            module = match.group("module").strip()
            if module in imports:
                # Catch double import lines.
                imports[module] = imports[module].union(set(import_objects))
            else:
                imports[module] = set(import_objects)
            position = match.end()

    return imports


def find_files(dir_path):
    """Find all Python files under `dir_path`, recursively.

    :param dir_path: The path to a directory to search for Python files.
    :return: A sorted list of the paths of the files found under `dir_path`.
    """
    return sorted(
        glob.glob(os.path.join(dir_path, "**", "*.py"), recursive=True))


def get_python_module_path_for_file(file_path, python_path):
    """Return the Python module path for a given Python file.

    :param file_path: The file for which to calculate the Python module
        path.
    :param python_path: The Python path under which to search (e.g.
        os.getenv("PYTHONPATH")).
    :return: List
    """
    python_paths = python_path.split(":")
    split_path = None

    for python_path in python_paths:
        if not file_path.startswith(python_path):
            continue

        # Remove `python_path` from the file path.
        python_path_len = len(python_path)
        if not python_path.endswith(os.path.sep):
            python_path_len += 1

        file_path = file_path[python_path_len:]
        file_path = (
            file_path
            .replace(".py", "")
            .replace("__init__", "")
            .strip(os.path.sep)
        )
        split_path = file_path.split(os.path.sep)
        return split_path
    else:
        raise ValueError(
            "Import Guardian was unable to determine a Python module "
            "path for '{}'. Is the file on your PYTHONPATH?".format(
                file_path))


def get_forbidden_imports(config, file_name, python_path):
    """Return a list of all the forbidden imports found in `file_name`.

    :param config: A dictionary-like object mapping
        python-imports-which-are-forbidden to the modules from which they
        may not be imported.
    :param file_name: The path to the file in which to look for
        forbidden imports.
    :param python_path: The python path to use when calculating module
        paths (e.g. os.getenv("PYTHONPATH")).
    """
    with open(file=file_name, encoding="ISO-8859-1", mode="r") as file_:
        file_imports = find_imports(file_.read())

    python_module_path = ".".join(
        get_python_module_path_for_file(file_name, python_path))

    fully_qualified_imports = set()
    for module, children in file_imports.items():
        if children:
            # If there are children, ensure that they get joined with
            # their parent module and added to the
            # fully_qualified_imports set.
            fully_qualified_imports = fully_qualified_imports.union(set(
                ".".join([module, child]) for child in children
            ))
        else:
            # Add the 'parent' import -- which will be a simple
            # 'import...' statement.
            fully_qualified_imports.add(module)

    forbidden_modules = config.get("forbidden_modules", {})
    forbidden_imports = []
    for forbidden_module, forbidden_module_config in forbidden_modules.items():
        forbidden_module = forbidden_module.replace(".*", "")
        forbidden_from = forbidden_module_config.get("forbidden_from", [])
        import_location_is_forbidden = (
            python_module_path in forbidden_from or
            any(
                python_module_path.startswith(forbidden_path)
                for forbidden_path in forbidden_from
            )
        )
        if not(import_location_is_forbidden or
                FORBIDDEN_FROM_WILDCARD in forbidden_from):
            continue

        for import_ in fully_qualified_imports:
            if import_.startswith(forbidden_module):
                forbidden_imports.append((file_name, import_))

    return forbidden_imports


def get_args():
    """Return an ArgumentParser containing the parsed args for this process."""
    parser = ArgumentParser()
    parser.usage = dedent("""\
        A static-analysis import guardian for Python. Exits with an
        error state if code being analysed contains imports which are
        explictly disallowed.

        Usage: import-guardian [-h] [-c CONFIG_FILE] [-p PYTHON_PATH] target
    """)
    parser.add_argument(
        "-c", "--config-file",
        default=os.path.join(os.getcwd(), "importguardian.json"),
        required=False, type=str, help=(
            "The path to the importguardian.json file containing the "
            "config for the current run of the import guardian. "
            "If not provided, the import guardian will try to find "
            "importguardian.json in the current working directory."))
    parser.add_argument(
        "-p", "--python-path", required=False, type=str, help=(
            "The Python Path to use when searching for forbidden imports. "
            "If not provided, this will default to the same directory as "
            "the `target` argument."
        ))
    parser.add_argument(
        "target", type=str, help=(
            "The file or directory to check for forbidden imports."))
    args = parser.parse_args(sys.argv[1:])

    if not args.python_path:
        args.python_path = args.target

    return args


def get_config(config_file):
    """Load the config JSON file and return it as a dict."""
    with open(config_file, "r") as config_file:
        return json.loads(config_file.read())


def main():
    """Run the Import Guardian."""
    args = get_args()

    try:
        config = get_config(args.config_file)
    except FileNotFoundError:
        print(
            "Couldn't find config file at {}. Does the file exist?".format(
                args.config_file),
            file=sys.stderr
        )
        # This `return` may look odd, but it's here to ensure that we
        # actually exit this function in testing.
        return sys.exit(2)

    forbidden_imports = []
    for file_path in sorted(find_files(args.target)):
        file_imports = get_forbidden_imports(
            config, file_path, args.python_path)
        forbidden_imports.extend(file_imports)

    if not forbidden_imports:
        return

    for forbidden_import_file, forbidden_import in forbidden_imports:
        sys.stderr.write(
            "{} may not be imported in {}\n".format(
                forbidden_import, forbidden_import_file)
        )
    sys.exit(1)
