#!/usr/bin/env python3

"""
# pushall
# push all local git repositories
# in my home directory.
# 2025-09-11: started by David Cary
"""

"""
FIXME: perhaps add a --dry-run option
that carefully avoids actually changing anything,
only listing what it *would* have done.
(perhaps initially the default,
followed by
"Do you want to continue? [Y/n] "
)
"""

import subprocess
import glob
import os

def push_one_git_folder(repo_folder):
    """
    This folder
    is likely a git repository --
    if it is, and we successfully push it,
    and it is "clean", print the complete success message.
    Otherwise do nothing but print
    an appropriate message about the status of this folder
    ("Not a repo I recognize (mercurial or git)";
    "unclean git repo";
    etc.
    ).
    """
    try:
        os.chdir(repo_folder)
    except FileNotFoundError:
        print( os.getcwd() )
        print("Whoops! Apparently ", repo_folder,
            "isn't a folder I can go to from here."
            )
        return

    print( os.getcwd() )
    result = subprocess.run([
        "git",
        "push",
        ],
        text=True, # FUTURE: ???
        # put outputs in result, rather than printing them immediately
        capture_output=True,
        )
    print( "pushed!" )
    print( result.stderr );

def push_all_git_repos(folder):
    print("looking for repos in: ", folder)
    # blindly try *all* subfolders
    # immediately under the given folder
    # list one per line
    try:
        os.chdir(folder)
    except FileNotFoundError:
        print( os.getcwd() )
        print("Whoops! Apparently ",
            folder,
            "isn't a folder I can go to from here."
            )
        return
    result = subprocess.run([
        "ls",
        "1", # one item per line
        ],
        text=True, # FUTURE: ???
        # put outputs in result, rather than printing them immediately
        capture_output=True,
        )
    potential_repo_string = result.stdout
    # assume no newlines in file names
    potential_repos = potential_repo_string.splitlines()
    for i in potential_repos:
        print(i)
    return

def main():
    version = "0.2025.1.00000" # FUTURE: append git commit hash?
    printf( "pushall version ", version )
    subprocess.run(["date"])
    """
    FIXME:
    by default, assume *this* file is in a git repo,
    assume that the ".." folder containing *this* git repo
    also directly contains a bunch of other git repos,
    and that the user wants to push all of those repos.
    Consider using
        cd $(git rev-parse --show-toplevel)
    (as recommended by
    "How To Navigate To The Git Root Directory?"
    https://www.geeksforgeeks.org/git/how-to-navigate-to-the-git-root-directory/
    )
    as part of the process to find those repos.
    """
    repofolders = [
            "~/Documents",
            # "/media/sf_Documents/",
            ]
    """
    Rather than the above hard-wired list,
    perhaps use a json config file
    like
    https://github.com/Catfriend1/syncthing-android/blob/main/wiki/Sync-N-first-files-get-N-movies-for-watching.md
    """
    for folder in repofolders:
        push_all_git_repos(folder)
    subprocess.run(["date"])
    print("done!")

if __name__ == "__main__":
    main()


# as recommended by https://wiki.python.org/moin/Vim :
# vim: set tabstop=8 expandtab shiftwidth=4 softtabstop=4 ignorecase :

