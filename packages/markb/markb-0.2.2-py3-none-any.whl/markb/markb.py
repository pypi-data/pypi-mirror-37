#!/usr/bin/env python3
# markb
# Get a markdown file via argument and output to a tempfile.
# Open automatically with browser. Fun!

from argparse import ArgumentParser
from tempfile import NamedTemporaryFile
from os import listdir
from os.path import isfile
import webbrowser

from markdown import markdown

__version__ = "0.2.2"

class ReadmeFilenameNotDetected(Exception):
    pass


def detect_readme_filename(filenames):
    for name in filenames:
        substr_to_check = name[:6].lower()
        if substr_to_check == "readme":
            return name
    
    raise ReadmeFilenameNotDetected()

def main():
    description = """Render markdown files to
    a temporary file and open it in a browser (YOUR browser!)"""
    parser = ArgumentParser(description=description)
    parser.add_argument("filename",
                        help="A markdown file",
                        nargs="?")
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + __version__)
    args = parser.parse_args()

    readme_filename = args.filename
    if readme_filename is None:
        try:
            filenames = [name for name in listdir() if isfile(name)]
            readme_filename = detect_readme_filename(filenames)
        except ReadmeFilenameNotDetected:
            exit("Can't detect a README file in here.")

    try:
        with open(readme_filename) as md:
            html = markdown(md.read())

        tempfile = NamedTemporaryFile(mode="w+", delete=False, suffix=".html")
        tempfile.write(html)
        webbrowser.open("file://{}".format(tempfile.name))

    except FileNotFoundError:
        print('File not found "{filename}"'.format(filename=args.filename))


if __name__ == "__main__":
    main()
