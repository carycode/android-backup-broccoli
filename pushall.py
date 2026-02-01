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

class FolderClass:
    def __init__(self):
        fullpath = ""
        is_git_repo = False
        pass

class FileClass:
    def __init__(self):
        fullpath = ""
        bytesize = 0
        name = ""
        

def size_of_folder_M(folder):
    """
    FUTURE: 
        import shutil
        total, used, free = shutil.disk_usage(path)
    """
    result = subprocess.run([
        "du",
        # "--human-readable", # output like "5.0G\tPhotos"
        "--block-size=1M", # output like "5078\tPhotos"
        "--summarize",
        # "--threshold=1G", # exclude entries smaller than 1G
        folder,
        ],
        text=True, # FUTURE: ???
        # put outputs in result, rather than printing them immediately
        capture_output=True,
        )
    assert ("" == result.stderr), "I expected stderr to be empty..."
    # ...split("None", ...) splits on runs of consecutive whitespace
    # where tabs, spaces, etc. are considered whitespace.
    words = result.stdout.split(None, 1)
    size_M = int(words[0])
    debug = True
    if( debug ):
        print( result.stderr );
        print( f"{size_M=}" )   
        pass
    return size_M

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
        folder_size_M = size_of_folder_M( repo_folder )
    except FileNotFoundError:
        print( os.getcwd() )
        print("Whoops! Apparently ", repo_folder,
            "isn't a folder I can go to from here."
            )
        return

    current_folder = os.getcwd()
    assert (
        current_folder ==
        repo_folder), f"Ooops, expected {current_folder=} == {repo_folder=}"

    print( f"{folder_size_M=}")

    result = subprocess.run([
        "git",
        "push",
        ],
        text=True, # FUTURE: ???
        # put outputs in result, rather than printing them immediately
        capture_output=True,
        )
    if( "Everything up-to-date" == result.stderr.strip() ):
        """
        FIXME: sometimes git says this even when there's uncommitted files
        (in a subfolder)
        i.e., even though "everything" is up-to-date,
        sometimes running "git status"
        says
            ...
            
            Untracked files:
              (use "git add <file>..." to include in what will be committed)
            ...
            
            nothing added to commit but untracked files present (use "git add" to track) 
        and other times "git status"
        says
            ...            
            nothing to commit, working tree clean
        ...
        FUTURE: how to handle these 2 cases?
        """
        print( f"push success! {repo_folder=}" )
        
        
        status_result = subprocess.run([
            "git",
            "status",
            "--untracked"
            ],
            text=True, # FUTURE: ???
            # put outputs in result, rather than printing them immediately
            capture_output=True,
            )
        if( -1 != status_result.stdout.find("Untracked files:") ):
            print( f"Untracked files in {repo_folder=}")
            print( f"{status_result.stderr=}" );
            print( f"{status_result.stdout=}" );
            pass
        elif( -1 != status.result.stdout.find("Changes not staged") )
            print( f""Changes not staged" in {repo_folder=}")
            print( f"{status_result.stderr=}" );
            print( f"{status_result.stdout=}" );
            pass
        else:
            #TODO: ??
            # FIXME: ??
            print( f"{status_result.stderr=}" );
            print( f"{status_result.stdout=}" );
            print( f"... [FIXME:] ... {repo_folder=}" )
            pass        

        pass
    elif( result.stderr.startswith("fatal: detected dubious ownership in repository") ):
        print( result.stderr );
        print( f"dubious ownership, skipping {repo_folder=}" )   
        pass
    elif( result.stderr.startswith("fatal: not a git repository") ):
        # print( result.stderr );
        print( f"not a git repository, skipping {repo_folder=}" ) 
        pass
    else:
        #TODO: ??
        #FIXME: ?
        print( f"{result.stderr=}" );
        print( f"{result.stdout=}" );
        print( f"... [FIXME:] ... {repo_folder=}" )
        pass
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
            os.path.abspath("/media/sf_Docs/t/"),
            os.path.abspath("/media/sf_Docs/"),
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

