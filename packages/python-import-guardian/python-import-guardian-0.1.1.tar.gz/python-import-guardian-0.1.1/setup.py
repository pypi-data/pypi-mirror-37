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
"""setup.py script for python-import-guardian."""

from distutils.core import setup

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setup(
    author="Graham Binns",
    author_email="graham@outcoded.uk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    description="A static-analysis Python import guardian.",
    download_url=(
        "https://gitlab.com/gmb/python-import-guardian/-/archive/master/"
        "python-import-guardian-master.tar.gz"
    ),
    entry_points={
        "console_scripts": [
            "import-guardian = importguardian.importguardian:main",
        ]
    },
    keywords=["import", "guardian", "static-analysis"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="python-import-guardian",
    packages=["importguardian"],
    url="https://gitlab.com/gmb/python-import-guardian",
    version="0.1.1",
)
