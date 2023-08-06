"""Main file for the Update Server application."""
import sys
import graphcall
import os

from . import calls
from . import utils

class Application(object):
    """Class defining the Update Server application."""

    def __init__(self, title):
        """Initialize the application."""
        self.title = title

    def exit_on_error(self, error):
        """Exit the application on error."""
        sys.stderr.write("{0}: {1}".format(self.title, str(error)))
        sys.exit(84)

    def get_present_mods(self, mods_folder: str):
        """Get the already present mods in the folder."""
        mods = os.listdir(mods_folder)
        return list(filter(lambda x: x[-4:] == ".jar", mods))

    def delete_present_entries(self, revisions_mods, files):
        """Delete the present entries."""
        revision_md5 = [mod["md5"] for mod in revisions_mods]
        md5s = list(map(utils.compute_md5, files))
        for index, md5 in zip(range(len(md5s)), md5s):
            if md5 not in revision_md5:
                print("Removing {}".format(files[index]))
                os.remove(files[index])
            else:
                revisions_mods.pop(revision_md5.index(md5))
                revision_md5.pop(revision_md5.index(md5))


    def download_mods(self, revision_mods, mod_folder):
        """Download the mods."""
        for mod in revision_mods:
            print("Downloading {}".format(mod["url"].split("/")[-1]))
            utils.download_file(mod["url"], mod_folder)

    def delete_all_folders_in(self, files_folder):
        """Delete all folders in the folder."""
        for file in os.listdir(files_folder):
            if os.path.isdir(files_folder + os.sep + file):
                utils.delete_folder(files_folder + os.sep + file)

    def run(self):
        """Run the application."""
        revision = sys.argv[1] if len(sys.argv) - 1 else calls.get_last_rev()
        mods_folder = sys.argv[2] if len(sys.argv) - 2 > 0 else "mods"
        if not os.path.exists(mods_folder):
            os.makedirs(mods_folder)
        revision_mods = calls.get_mods(revision)
        presents_mods = self.get_present_mods(mods_folder)
        files = list(map(lambda x: mods_folder + os.sep + x, presents_mods))
        self.delete_present_entries(revision_mods, files)
        self.download_mods(revision_mods, mods_folder)
        self.delete_all_folders_in(mods_folder)
        print("Complete !")


def main():
    """Update the server."""
    app = Application("Update Server")
    app.run()
