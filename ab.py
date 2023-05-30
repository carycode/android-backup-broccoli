#!/usr/bin/env python3

"""
ab.py : android backup

backup photos to github

WARNING: version  2023.00.01-alpha : extremely rough draft.

Initial testing:
    Ubuntu 22 (LTS)
    Galaxy Note10

https://github.com/carycode/android-backup-broccoli

# normal use

[FIXME]

# features

* idempotent: after running once,
running again effectively does nothing
(until new photos are discovered on phone)
* incremental / interruptible:
the phone can be unplugged at any time,
and running it later
will be able to recover and resume.
* respectful: 
"We recommend repositories remain small,
ideally less than 1 GB, and
less than 5 GB is strongly recommended." and
"GitHub limits the size of files allowed in repositories. If you attempt to add or update a file that is larger than 50 MB, you will receive a warning from Git." --
https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github

We should stay well away from the
"remote: fatal: pack exceeds maximum allowed size (2.00 GiB)"
error message.

* tolerant: supports *both* running the program and then plugging in the phone, as well as plugging in the phone and then running the program
* tolerant: supports "finishing up" photos buffered locally after the phone is unplugged.


# installation and initial setup

[FIXME]

# etc.

2023-05-24: started by David Cary


MTP seems to "just work" under Ubuntu 22 (LTS),
and so all the tips in
"Getting MTP enabled devices to work with Ubuntu?"
https://askubuntu.com/questions/87667/getting-mtp-enabled-devices-to-work-with-ubuntu
seems to be no longer necessary.


"""


"""
FUTURE:
add logging, perhaps
https://python-docs.readthedocs.io/en/latest/writing/logging.html

FUTURE:
    consider using
    GitPython
    as recommended by
    https://stackoverflow.com/questions/15315573/how-can-i-call-git-pull-from-within-python
Currently using simple subprocess calls instead of GitPython,
as recommended by
https://stackoverflow.com/questions/11113896/use-git-commands-within-python-code

"""

import os
import subprocess
from time import sleep


def get_folder_size_M(repo_path=None):
    # using "du" for historical reasons;
    # many other approaches are mentioned in
    # https://stackoverflow.com/questions/1392413/calculating-a-directorys-size-using-python
    print("getting folder size ...")
    result = subprocess.run([
        "du",
        "--summarize",
        "--block-size=1M", # in units of 1 MByte (1024*1024)
        # (rather than default units of 1024 bytes)
        repo_path
        ],
        text=True, # FUTURE: ???
        capture_output=True # put outputs in result, rather than printing them immediately
        )
    print( result.stderr );
    size_string = result.stdout
    print( size_string );
    # gives something like "2180438\t../.git"
    # we assume there's whitespace immediately after the digits.
    number = int(size_string.split()[0])
    return number

def round_up( x, y ):
    # plain "//" rounds toward -inf;
    # negate twice to round toward +inf.
    result = -(-x // y)
    assert( type(result) is int )
    return result


def get_unstaged_photos(photo_dir=None):
    # Future: perhaps 
    # look at all the photos in the folder
    #   photo_list = os.listdir(photo_dir)
    # in order to sort into
    # appropriate folders.


    # only "untracked" files
    # (files that have not yet been committed)
    result = subprocess.run([
        "git",
        "ls-files",
        "--others", # the other (untracked) files
        "--exclude-standard"
        ],
        text=True, # FUTURE: ???
        capture_output=True # put outputs in result, rather than printing them immediately
        )
    print( result.stderr );
    untracked_file_string = result.stdout
    # assume no newlines in file names
    untracked_files = untracked_file_string.splitlines()
    return untracked_files


def push_to_remote(repo_path=None, date_range=None):
    if(repo_path):
        print("Current working directory: ")
        print( os.getcwd() )
        os.chdir('/tmp')
        os.chdir(repo_path)
        print( os.getcwd() )
        subprocess.run(["git", "push"])
        print( "pushed!" )

        # consider adding another file,
        # but only if
        # (a) repo will be less than 5 GB
        # (perhaps rough estimate
        # (current_size + 0.1 GB + 2 * file_size < 5 GB) ?
        # and
        # (b) each file is less than 50 MB
        # and
        # (c) it's in the date range for this repository.
        untracked_files = get_unstaged_photos()
        print(len(untracked_files), "untracked files.")
        verbose = False
        if(verbose):
            print(repr(untracked_files))

        # FUTURE:
        # untracked_total_size_M = total_size_M(untracked_files)

        # This assumes we're
        # exactly 1 subdirectory deep in the repo.
        # FUTURE: handle other locations in the repo
        # (the root of the repo, or
        # nested 2 deep, or etc.
        # ).
        git_folder_size_M = get_folder_size_M("../.git")
        print("git folder size: ", git_folder_size_M, " MByte.")



        # Are there any untracked files?
        # (pythonic idiom, see
        # https://stackoverflow.com/questions/53513/how-do-i-check-if-a-list-is-empty
        # for details).
        while( untracked_files ):
            print("")
            the_file = untracked_files[0]
            # On my phone,
            # file names look something like:
            # "20210528_100040.jpg"
            print("considering file: ", the_file)

            file_size = os.path.getsize( the_file )
            file_stat = os.stat( the_file )
            file_size_b = file_stat.st_size
            assert( file_size_b == file_size )
            file_size_M = round_up( file_size, (1024*1024) )
            print("with file size: ", file_size_M, " MByte")
            do_it = True
            if( ".jpg" != the_file[-4:] ):
                # only photos (*.jpg)
                print( the_file,
                    " doesn't seem to be a photo; skipping."
                    )
                do_it = False;
            if( file_size_M >= 50 ):
                # that are less than 50 MB
                print( the_file,
                    " seems to be too large: ",
                    file_size_M, " MByte."
                    )
                do_it = False;
            if( date_range and not
                (date_range[0] < the_file <= date_range[1])
                ):
                print( the_file,
                    " Doesn't seem to be in the range ",
                    date_range
                    )
                do_it = False;
            max_repo_size_M = 2500 # ???? FUTURE: ????
            git_folder_size_M += file_size_M
            if( git_folder_size_M > max_repo_size_M):
                print(
                    "repo too large; it's already ",
                    git_folder_size_M,
                    " MBytes."
                    )
                do_it = False;
            if( do_it ):
                if(verbose):
                    print("adding ", the_file)
                subprocess.run(["git", "add",
                    # "--dry-run",
                    the_file])
                if(verbose):
                    print("committing ", the_file)
                # avoid printing the lengthy status info
                # (such as every untracked file)
                # that the 'git commit' command produces.
                result = subprocess.run(
                    ["git", "commit",
                    # "--dry-run",
                    "-m", "add photo"],
                    text=True, # FUTURE: ???
                    capture_output=True # put outputs in result, rather than printing them immediately
                    )
                print( result.stderr );
                if(verbose):
                    print( result.stdout )
                if(verbose):
                    print("pushing ", the_file)
                subprocess.run(["git", "push",
                    # "--dry-run"
                    ])
                print( the_file, " pushed!" )
            # FUTURE:
            # perhaps pull another photo
            # from phone?
            print("sleeping ...")
            sleep(10) # seconds
            # remove first item from array
            # (possibly leaving it empty).
            untracked_file = untracked_files[1:]




def pull_from_phone(phone_path=None):
    if(phone_path):
        print("Using phone path: ")
        print(phone_path)
        # FIXME:


def main(repo_path=None, phone_path=None, date_range=None):
    print("starting ab...")
    # FUTURE:
    # consider supporting
    # several repositories.
    # Then somehow deciding,
    # from the date-time stamp on each photo,
    # which respository
    # to push it to.

    push_to_remote(repo_path, date_range)
    pull_from_phone(phone_path)

    print("done!")

if __name__ == "__main__":
    r_path = "/media/sf_t/n/2021-friendly-octo-disco/2021_b/"
    r_path = "/media/sf_t/k/2021-turbo-tube-memory/2021"
    d_range = ["202105", "20210531"]
    # inspired by
    # "Accessing MTP mounted device in terminal"
    # https://unix.stackexchange.com/questions/464767/accessing-mtp-mounted-device-in-terminal
    p_path = "/run/user/1000/gvfs/mtp:host=SAMSUNG_SAMSUNG_Android_R58MC496J4W/Internal storage/DCIM/Camera"
    main(
        repo_path = r_path,
        phone_path = p_path,
        date_range = d_range
        )

# as recommended by https://wiki.python.org/moin/Vim :
# vim: set tabstop=8 expandtab shiftwidth=4 softtabstop=4 :

