#!/usr/bin/env python3

"""
ab.py : android backup
README.md

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
    https://gitpython.readthedocs.io/
    as recommended by
    https://stackoverflow.com/questions/15315573/how-can-i-call-git-pull-from-within-python
Currently using simple subprocess calls instead of GitPython,
as recommended by
https://stackoverflow.com/questions/11113896/use-git-commands-within-python-code

FUTURE:
Perhaps attempt to commit many or all the photos at once;
then if something goes wrong,
undo that commit
and retry with half as many photos
only giving up
when it's been reduced to 1 photo
and even that doesn't work.
Perhaps using the "undo commit" approach
described in
* "You just committed a large file and can't push to GitHub"
https://lcolladotor.github.io/2020/03/18/you-just-committed-a-large-file-and-can-t-push-to-github/
and
* "How do I undo the most recent local commits in Git?"
https://stackoverflow.com/questions/927358/how-do-i-undo-the-most-recent-local-commits-in-git


"""

import os
import subprocess
from time import sleep
import glob


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

def get_file_size_M(the_file=None):
    # FUTURE: pick one method, rather than both
    file_size = os.path.getsize( the_file )
    file_stat = os.stat( the_file )
    file_size_b = file_stat.st_size
    assert( file_size_b == file_size )
    file_size_M = round_up( file_size, (1024*1024) )
    return file_size_M

def total_files_size_M(file_list):
    # FIXME
    return 0

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
        try:
            os.chdir(repo_path)
        except FileNotFoundError:
            print( os.getcwd() )
            print("whoops! can't find: ", repo_path)
            return
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

        max_repo_size_M = 2500 # ???? FUTURE: ????

        if(1):
            files_size_M = total_files_size_M(untracked_files)
            estimated_total = git_folder_size_M + files_size_M
            print(
                "Considering adding about",
                files_size_M,
                " MByte more untracked files.",
                " Estimated total: ",
                    estimated_total,
                " MByte."
                )
            if( estimated_total > max_repo_size_M):
                print(
                    "Estimated total repo: ",
                    estimated_total,
                    "too large; it's already ",
                    git_folder_size_M,
                    " MBytes",
                    " and we're trying to add about",
                    files_size_M,
                    " more untracked files."
                    )
                return

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

            file_size_M = get_file_size_M(the_file)

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
            # remove first item from array
            # (possibly leaving it empty).
            untracked_files = untracked_files[1:]
            if(1): # if(verbose):
                print(len(untracked_files), "untracked files.")
            print("sleeping ...")
            sleep(10) # seconds




# FIXME:
# check how much free space is left,
# (perhaps with "df")
# and prematurely stop pulling photos after
# the "starting" free space is, say, half-full.
def pull_from_phone(phone_path=None):
    if(not phone_path):
        print("phone path: [", phone_path, "] empty -- skipping.")
        return
    if(phone_path):
        print("Using phone path: ")
        print(phone_path)
        try:
            os.chdir(phone_path)
        except FileNotFoundError:
            print("whoops! can't find: ", phone_path)
            print("Try unplugging the phone and plugging it in again.")
            print("Try restarting the phone.")
            return
        print("Found phone at: ")
        print( os.getcwd() )
        # FIXME:
        # "Cross-platform way of getting temp directory in Python"
        # https://stackoverflow.com/questions/847850/cross-platform-way-of-getting-temp-directory-in-python

        # FUTURE:
        # "How to rsync to android"
        # https://askubuntu.com/questions/343502/how-to-rsync-to-android
        dest_temp_folder = "/media/sf_t/new/"
        dest_temp_folder = "/media/sf_t/2021-potential-octo-guide/2021"
        dest_temp_folder = "/media/sf_t/new10/"
        """
        source_file_pattern = os.path.join(
                phone_path, 
                "20210" +
                "*.jpg"
                )
        """
        source_file_pattern = "20211[0-9]*.jpg"
        source_file_pattern = "2021[0-1][0-9]*.jpg" # works!
        source_file_pattern = "20220[0-1]*.jpg"
        print("Using file pattern: ", source_file_pattern)
        photo_files = glob.glob(source_file_pattern)
        print("Found ", len(photo_files), " files.")
        photo_files.sort()
        print( photo_files )
        print("Found ", len(photo_files), " files.")
        if(photo_files):
            for the_file in photo_files:
                print("moving ",
                        the_file,
                        " to ",
                        dest_temp_folder
                    )
                # FIXME:
                # how to decide
                # which files to move ("mv")
                # and which files to copy ("cp") ?
                subprocess.run(["mv",
                    the_file,
                    dest_temp_folder
                    ])
                sleep(1) # seconds
        else:
            print( photo_files, "no files found.")
    print("... done pulling from phone.")


"""
If temporary folder is *empty*,
we want to pull from the *phone* first
(perhaps into temporary folder?).

If temporarary folder is *not* empty,
we want to make sure the local repo
is finished
committing all files,
(perhaps and also
syncing with remote repo,
),
*then*
move file in the appropriate range (if any)
from the temp folder
to the local repo,
(and of course
then syncing with remote repo
).

If some file is mangled,
what we *don't* want to do
is keep only the mangled version
and throw away any other versions.
At first,
we keep all versions
in separate folders.
Later,
we'll
*inform* the user that mangling was detected,
(how exactly???)
and in the most common case
(one first is the *start* of the file,
the rest was somehow truncated
).
Perhaps:
(a) commit the short, truncated version of the file,
then
(b) commit the next-longer version of the file
until there are no remaining versions.

"""
def sort_from_one_temp(temp_path=None, repo_path=None, date_range=None):
    print("Sorting from ",
            temp_path,
            " to ",
            repo_path,
            " with date_range ",
            date_range,
            "...")
    all_exist = temp_path and repo_path and date_range
    if(not all_exist):
        print("temp path:", temp_path, " skipping.")
        print("repo path:", repo_path, " skipping.")
        print("date range:", date_range, " skipping.")
        return
    if(repo_path):
        print("Using repo path: ")
        print(repo_path)
        try:
            os.chdir(repo_path)
        except FileNotFoundError:
            print("whoops! can't find repo path: ", repo_path)
            return
        print("Found it at: ")
        print( os.getcwd() )
    if(temp_path):
        print("Using temp path: ")
        print(temp_path)
        try:
            os.chdir(temp_path)
        except FileNotFoundError:
            print("whoops! can't find temp path: ", temp_path)
            return
        print("Found it at: ")
        print( os.getcwd() )
        # FIXME: better representation of date range ...
        source_file_pattern = os.path.join(
                temp_path, 
                "2021" +
                "*.jpg"
                )
        print("Using source file pattern: ", source_file_pattern)
        photo_files = glob.glob(source_file_pattern)
        print("Found ", len(photo_files), " files.")
        if( not photo_files ):
            print( "photo_files: ",
                photo_files, " no files found.")
            return
        photo_files.sort()
        print( [
            photo_files[0],
            " ... ",
            photo_files[-1]
            ]
            )
        # prints something like
        # ['/media/sf_t/new10/20210324_104944.jpg',
        # ' ... ',
        # '/media/sf_t/new10/20210529_101807(0).jpg']
        print("Found ", len(photo_files), " files.")
        dest_file_pattern = os.path.join(
                repo_path,
                "*.jpg"
                )
        print("Using repo file pattern: ", dest_file_pattern)
        dest_files_full = glob.glob(dest_file_pattern)
        dest_files_full.sort()
        if(dest_files_full):
            print(
                "dest_files_full: ",
                [
                dest_files_full[0],
                " ... ",
                dest_files_full[-1]
                ]
                )
        # prints something like
        # ['/media/sf_t/2021-cautious-enigma/2021/20210529_101817.jpg',
        # '...',
        # '/media/sf_t/2021-cautious-enigma/2021/20210531_114749.jpg']

        # Use os.path.basename() to convert to
        # just the file names (without the path):
        # ['20210529_101817.jpg',
        # '...',
        # '20210531_114749.jpg']
        dest_files = map(os.path.basename, dest_files_full)
        # Use "list()" in order to avoid the
        # "TypeError: 'map' object is not subscriptable" error.
        # https://stackoverflow.com/questions/1303347/getting-a-map-to-return-a-list-in-python-3-x
        dest_files = list(dest_files)
        if(dest_files):
            print(
                "dest_files: ",
                [
                dest_files[0],
                " ... ",
                dest_files[-1]
                ]
                )
        for the_file_full in photo_files:
            the_file_name = os.path.basename(the_file_full)
            in_range = (
                date_range[0] < the_file_name <= date_range[1]
                )
            if( the_file_name in dest_files ):
                print("whoops, ",
                    the_file_full,
                    " already in ",
                    dest_file_pattern
                    )
            else:
                if(in_range):
                    print("moving ", the_file_full)
                    subprocess.run(["mv",
                        the_file_full,
                        repo_path
                        ])
                    sleep(1) # seconds
    print("... done sorting from ",
            temp_path,
            " to ",
            repo_path,
            ".")

def sort_from_temps():
    """ in addition to moving files
    from temp folder(s) to appropriate repos,
    also detect duplicate file names,
    to avoid overwriting.
    """
    sort_from_one_temp(temp_path, repo_path, date_range)

"""
# FIXME:
Support several "temp source" folders
in addition to mounting the camera as a folder,
in case some photos
have already been pulled from the camera
into a "temp source" folder.
Move photos from the source
to the git repo,
but only if they're in the correct range.

# FIXME:
If we have a bunch of photos
that go into a repo
that exists on github,
but doesn't exist locally,
perhaps clone that repo locally first.

# FIXME:
perhaps
encode the range
in the repo itself,
perhaps in a text file?

# FIXME:
both of the above sound great,
but if we try to implement *both*,
how do we know *which* repo a photo goes into?
(I.e.,
avoid the catch-22 of
we need to know which repo a photo goes into
in order to decide which one to clone,
but
we need to clone the repo first
before we get the self-describing text file
that tells which range of photos it contains.
).
Perhaps:
Each repo contains not only its own range,
but also
a list of a few "nearby"
repos and their ranges.

"""

def handle_one_repo(repo_path=None, phone_path=None, date_range=None):
    print("starting handle_one_repo...")
    subprocess.run(["date"])
    # FUTURE:
    # consider supporting
    # several repositories.
    # Then somehow deciding,
    # from the date-time stamp on each photo,
    # which respository
    # to push it to.

    push_to_remote(repo_path, date_range)
    pull_from_phone(phone_path)

    subprocess.run(["date"])
    print("done!")

def handle_repos():
    r_path = "/media/sf_t/2021-cuddly-octo-broccoli/2021/"
    d_range = ["202101", "20210399"]
    handle_one_repo(
        repo_path = r_path,
        date_range = d_range
        )

    """
    # FIXME: tip of current branch is behind its remote counterpart
    r_path = "/media/sf_t/2021-friendly-octo-disco/2021_b/"
    d_range = ["202104", "20210499"]

    r_path = "/media/sf_t/2021-turbo-tube-memory/2021"
    d_range = ["202105", "20210529"]
    handle_one_repo(
        repo_path = r_path,
        date_range = d_range
        )
    """

    r_path = "/media/sf_t/2021-cautious-enigma/2021"
    d_range = ["20210529", "20210599"]
    temp_folder = "/media/sf_t/new10/"
    handle_one_repo(
        repo_path = r_path,
        date_range = d_range
        )
    sort_from_one_temp(temp_folder, r_path, d_range)


    r_path = "/media/sf_t/2021-friendly-octo-goggles/2021"
    d_range = ["202106", "20210699"]
    handle_one_repo(
        repo_path = r_path,
        date_range = d_range
        )
    sort_from_one_temp(temp_folder, r_path, d_range)

    r_path = "/media/sf_t/2021-fuzzy-octo-sniffle/2021"
    d_range = ["202107", "20210726_99"]
    handle_one_repo(
        repo_path = r_path,
        date_range = d_range
        )
    sort_from_one_temp(temp_folder, r_path, d_range)

    r_path = "/media/sf_t/2021-fluke-redesigned-garbanzo/2021"
    d_range = ["20210727", "20210799"]
    handle_one_repo(
        repo_path = r_path,
        date_range = d_range
        )
    sort_from_one_temp(temp_folder, r_path, d_range)


    r_path = "/media/sf_t/2021-joke-expert-bassoon/2021"
    d_range = ["202108", "20210999"]
    handle_one_repo(
        repo_path = r_path,
        date_range = d_range
        )
    sort_from_one_temp(temp_folder, r_path, d_range)

    r_path = "/media/sf_t/2021-potential-octo-guide/2021"
    d_range = ["202110", "20211299"]
    handle_one_repo(
        repo_path = r_path,
        date_range = d_range
        )


    r_path = "/media/sf_t/2022-silver-carnival-dross/2022"
    d_range = ["202200", "20220199"]
    handle_one_repo(
        repo_path = r_path,
        date_range = d_range
        )

    # inspired by
    # "Accessing MTP mounted device in terminal"
    # https://unix.stackexchange.com/questions/464767/accessing-mtp-mounted-device-in-terminal
    # "Where are MTP mounted devices located in the filesystem?"
    # https://askubuntu.com/questions/342319/where-are-mtp-mounted-devices-located-in-the-filesystem
    # "What is the Android phone MTP mount point in (K)ubuntu 20.04 if not /run/user/1000/gvfs?"
    # https://askubuntu.com/questions/1339104/what-is-the-android-phone-mtp-mount-point-in-kubuntu-20-04-if-not-run-user-10
    p_path = "/run/user/1000/gvfs/mtp:host=SAMSUNG_SAMSUNG_Android_R58MC496J4W/Internal storage/DCIM/Camera"
    # The path for my phone includes ":" and a space.
    # But it appears I don't need to use "glob.escape".
    handle_one_repo(
        repo_path = r_path,
        phone_path = p_path,
        date_range = d_range
        )

if __name__ == "__main__":
    subprocess.run(["date"])
    p_path = "/run/user/1000/gvfs/mtp:host=SAMSUNG_SAMSUNG_Android_R58MC496J4W/Internal storage/DCIM/Camera"
    pull_from_phone(p_path)
    handle_repos()
    # sort_from_temps()
    sleep(10)
    pull_from_phone(p_path)
    sleep(30)
    pull_from_phone(p_path)
    subprocess.run(["date"])
    print("done!")


# as recommended by https://wiki.python.org/moin/Vim :
# vim: set tabstop=8 expandtab shiftwidth=4 softtabstop=4 ignorecase :

