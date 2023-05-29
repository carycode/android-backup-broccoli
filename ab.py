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

def get_unstaged_photos(photo_dir=None):
    photo_list = os.listdir(photo_dir)
    # only photos (*.jpg)
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
    untracked_files = result.stdout
    print("untracked files:")
    print(untracked_files)
    # FIXME:
    photo_list = []

def main(repo_path=None, phone_path=None, date_range=None):
    print("starting ab...")
    # FUTURE:
    # consider supporting
    # several repositories.
    # Then somehow deciding,
    # from the date-time stamp on each photo,
    # which respository
    # to push it to.
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
        unstaged_photos = get_unstaged_photos()
        print( "unstaged photos: ")
        print( unstaged_photos )

    if(phone_path):
        print("Using phone path: ")
        print(phone_path)

    print("done!")

if __name__ == "__main__":
    r_path = "/media/sf_t/n/2021-friendly-octo-disco/2021_b/"
    r_path = "/media/sf_t/k/2021-turbo-tube-memory/2021"
    # inspired by
    # "Accessing MTP mounted device in terminal"
    # https://unix.stackexchange.com/questions/464767/accessing-mtp-mounted-device-in-terminal
    p_path = "/run/user/1000/gvfs/mtp:host=SAMSUNG_SAMSUNG_Android_R58MC496J4W/Internal storage/DCIM/Camera"
    main(
        repo_path = r_path,
        phone_path = p_path,
        date_range = ["202104", "20210419"]
        )

# as recommended by https://wiki.python.org/moin/Vim :
# vim: set tabstop=8 expandtab shiftwidth=4 softtabstop=4 :

