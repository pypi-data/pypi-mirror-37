#!/usr/bin/env python3

"""
This script sets some symlinks inside the AsciiDoc3 package
installed via pip / pip3 from 'https://pypi.org/project/asciidoc3/'.
Run it immediately subsequently after install.
See https://asciidoc3.org/pypi.html for more information.

Copyright (C) 2018 by Berthold Gehrke <berthold.gehrke@gmail.com>
Free use of this software is granted under the terms of the
GNU General Public License Version 2 or higher (GNU GPLv2+).
"""

import os
import re
import subprocess
import sys

USERHOMEDIR = os.path.expanduser("~") # e.g. GNU/Linux: USERHOMEDIR = '/home/<username>'

def main():
    """
    runs "pip show asciidoc3" to locate AsciiDoc3's config-dirs and sets symlinks;
    at first within AsciiDoc3, than from the user's home directory.
    """
    ad3_location = ''
    try:
        runpip = subprocess.Popen("pip show asciidoc3", shell=True, stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1)
        runpip.wait()
        pip_show_status = runpip.returncode
        if pip_show_status:
            sys.exit("FATAL: 'pip show asciidoc3' ends with non-zero exit code")
        output = runpip.communicate()
    except OSError:
        sys.exit("FATAL: 'pip show asciidoc3' ends with an unidentified error ...")
    if output:
        output = output[0]
        output = re.split(r'Location: ', output, re.DOTALL)[1]
        output = re.split(r'\nRequires', output, re.DOTALL)[0]
        ad3_location = output
        # ad3_location <class 'str'> looks like this:
        # '/home/<username>/.local/lib/python3.5/site-packages'
    else:
        # no output
        sys.exit("FATAL: 'pip show asciidoc3' gives no information ...")

    # AsciiDoc3 distribution, set internal (relative) symlinks.
    # <...>/asciidoc3/filters/music/images --> ../../images
    if os.path.exists(ad3_location + "/asciidoc3/filters/music/images"):
        os.unlink(ad3_location + "/asciidoc3/filters/music/images")
    os.symlink(os.path.relpath(
        ad3_location + "/asciidoc3/images", ad3_location + "/asciidoc3/filters/music"),
               ad3_location + "/asciidoc3/filters/music/images")

    # <...>/asciidoc3/filters/graphviz/images --> ../../images
    if os.path.exists(ad3_location + "/asciidoc3/filters/graphviz/images"):
        os.unlink(ad3_location + "/asciidoc3/filters/graphviz/images")
    os.symlink(os.path.relpath(
        ad3_location + "/asciidoc3/images", ad3_location + "/asciidoc3/graphviz/music"),
               ad3_location + "/asciidoc3/filters/graphviz/images")

    # <...>/asciidoc3/doc/images --> ../images
    if os.path.exists(ad3_location + "/asciidoc3/doc/images"):
        os.unlink(ad3_location + "/asciidoc3/doc/images")
    os.symlink(os.path.relpath(
        ad3_location + "/asciidoc3/images", ad3_location + "/asciidoc3/doc"),
               ad3_location + "/asciidoc3/doc/images")

    # Set symlinks user home to AsciiDoc3's 'working/config' directories'
    # Skip if running as root.
    if USERHOMEDIR != '/root':
        if os.path.exists(USERHOMEDIR + "/.asciidoc3"):
            os.replace(USERHOMEDIR + "/.asciidoc3", USERHOMEDIR + "/.asciidoc3_backup")
        os.symlink(ad3_location + "/asciidoc3", USERHOMEDIR + "/.asciidoc3")

        if os.path.exists(USERHOMEDIR + "/asciidoc3"):
            os.replace(USERHOMEDIR + "/asciidoc3", USERHOMEDIR + "/asciidoc3_backup")
        os.symlink(ad3_location + "/asciidoc3", USERHOMEDIR + "/asciidoc3")

if __name__ == '__main__':
    main()
