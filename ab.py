#!/usr/bin/env python3

"""
ab.py : android backup

backup photos to github

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
* tolerant: supports *both* running the program and then plugging in the phone, as well as plugging in the phone and then running the program
* tolerante: supports "finishing up" photos buffered locally after the phone is unplugged.


# installation and initial setup

[FIXME]

# etc.

2023-05-24: started by David Cary

"""


def main():
    print("starting ab...")
    print("done!")

if __name__ == "__main__":
    main()

# as recommended by https://wiki.python.org/moin/Vim :
# vim: set tabstop=8 expandtab shiftwidth=4 softtabstop=4 :

