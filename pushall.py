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
    current_folder = os.getcwd()
    assert (current_folder ==
            repo_folder), f"Ooops, expected {current_folder=} == {repo_folder=}"
    result = subprocess.run([
        "git",
        "push",
        ],
        text=True, # FUTURE: ???
        # put outputs in result, rather than printing them immediately
        capture_output=True,
        )
    if( "Everything up-to-date" == result.stderr.strip() ):
        print( f"push success! {repo_folder=}" )
    else:
        #TODO: ??
        #FIXME: ?
        print( result.stderr );
        print( f"... [FIXME:] ... {repo_folder=}" )
    return

def push_all_git_repos(folder_of_repos):
    print("looking for repos in: ", folder_of_repos)
    # blindly try *all* subfolders
    # immediately inside the given folder
    # list one per line
    try:
        os.chdir(folder_of_repos)
    except FileNotFoundError:
        print( os.getcwd() )
        print("Whoops! Apparently ",
            folder_of_repos,
            "isn't a folder I can go to from here."
            )
        return
    current_folder = os.getcwd()
    assert (current_folder ==
            folder_of_repos), f"Ooops, expected {current_folder=} == {folder_of_repos=}"
    potential_repos = os.listdir( current_folder )
    for i in potential_repos:
        one_repo_folder = os.path.normpath( os.path.join( folder_of_repos, i ) )
        isdir = os.path.isdir( one_repo_folder )
        if(isdir):
            push_one_git_folder(one_repo_folder)
    return

def main():
    version = "0.2025.1.00000" # FUTURE: append git commit hash?
    print( "pushall version ", version )
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
            os.path.abspath("../"),
            os.path.expanduser("~/Documents/"),
            os.path.abspath("../Documents/"),
            # os.path.abspath("/media/sf_Documents/"),
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

