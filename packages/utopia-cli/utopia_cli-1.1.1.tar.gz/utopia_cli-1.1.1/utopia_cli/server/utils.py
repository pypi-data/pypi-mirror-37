"""Utility functions for using in the UtopiaCLI."""
import hashlib
import urllib.request
import urllib.parse
import os


def compute_version(revision: str) -> int:
    """Compute the version of the given revision."""
    try:
        major, minor, fix = revision.split(".")
    except ValueError:
        return 0
    return (
        (int(major) << 16) +
        (int(minor) << 8) +
        (int(fix))
    )


def compute_md5(file: str) -> str:
    """Compute the md5 of the given file."""
    with open(file, "rb") as fileToCompute:
        return hashlib.md5(fileToCompute.read()).hexdigest()


def download_file(url: str, folder: str):
    """Download the file and place it in the folder."""
    file = urllib.parse.unquote(url).split("/")[-1]
    urllib.request.urlretrieve(url, folder + os.sep + file)

def delete_folder(path: str):
    """Delete a folder."""
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
