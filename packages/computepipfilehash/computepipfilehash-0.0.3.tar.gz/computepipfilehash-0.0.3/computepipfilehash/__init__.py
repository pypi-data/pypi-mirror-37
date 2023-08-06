#!/usr/bin/env python3
import os
import sys
import json
import base64
import hashlib
import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--wheel-hashes', action='store_true')
    parser.add_argument('--update-hashes', action='store_true')
    args = parser.parse_args()
    if args.wheel_hashes:
        # First find all of wheels and their names
        if not os.path.exists("./localwheels/"):
            print("Missing localwheels directory.")
            sys.exit(3)
        files = os.listdir("./localwheels/")
        for filename in files:
            # We only want wheels here.
            if not filename.endswith(".whl"):
                continue
            fullpath, digest = calculate_digest(filename)
            print("{} --hash=sha256:{}".format(fullpath, digest))

    elif args.update_hashes:
        # Check if we have a requirements-build.txt for not.
        if not os.path.exists('requirements-build.txt'):
            print("First generate a requirements-build.txt file.")
            sys.exit(3)

        # We have a requirements-build.txt file
        with open("requirements-build.txt") as fobj:
            lines = fobj.readlines()

        files = os.listdir("./localwheels/")

        newlines = []
        for line in lines:
            line = line.strip()
            words = line.split()
            values = words[0].split("==")
            packagename = "-".join(values)
            othername = "-".join([values[0].replace("-", "_"), values[1]])

            for name in files:
                lowername = name.lower()
                if not lowername.endswith(".whl"):  # Only for wheels
                    continue
                package_othername = packagename.replace("-", "_")
                # Now check if a wheel is already available
                if lowername.startswith(packagename) or lowername.startswith(othername):
                    # Let us get the new hash of the wheel
                    _, digest = calculate_digest(name)
                    # Check if the sha256sum is already there or not
                    if digest not in line:
                        # Now add the hash to the line
                        line = "{} --hash=sha256:{}".format(line, digest)
            newlines.append(line)

        # Finally write the result back to the file
        with open("requirements-build.txt", "w") as fobj:
            fobj.write("\n".join(newlines))


    else:
        # Find the Pipfile.lock and create a requirements-build.txt with all hashes
        if not os.path.exists("Pipfile.lock"):
            print("Pipfile.lock file is missing in the current directory.")
            sys.exit(1)
        with open("Pipfile.lock") as fobj:
            data = json.load(fobj)

        defaults = data["default"]
        for name in defaults:
            package_name = "{}{}".format(name, defaults[name]["version"])
            hashes = " ".join(["--hash={}".format(value) for value in defaults[name]["hashes"]])
            print("{} {}".format(package_name,hashes))
                

def calculate_digest(filename):
    "Calculates the sha256sum of a given file"
    fullpath = os.path.join("./localwheels/", filename)
    with open(fullpath, "br") as fobj:
        data = fobj.read()

    # Now compute the hash
    digest = hashlib.sha256(data).hexdigest()
    return fullpath, digest


def download_sources():
    "Download the sources from PyPI"
    cmd = "pip3 download --no-binary :all: -d ./localwheels/ -r requirements-build.txt"
    output = subprocess.check_call(cmd.split())
    sys.exit(output)


def build_wheels():
    "Build the wheels from the local directory"
    cmd = "pip3 wheel --no-index --find-links ./localwheels/ -w ./localwheels/ -r requirements-build.txt"
    output = subprocess.check_call(cmd.split())
    sys.exit(output)


if __name__ == "__main__":
    main()
