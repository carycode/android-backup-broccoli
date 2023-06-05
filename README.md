# android-backup-broccoli
backup photos to github

# normal use


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


# installation and initial setup

[FIXME]


# etc.

# Related

* "You just committed a large file and can't push to GitHub"
https://lcolladotor.github.io/2020/03/18/you-just-committed-a-large-file-and-can-t-push-to-github/

* "#photo-sharing" topic on github
https://github.com/topics/photo-sharing

* "Use GitHub Repo to Host Images"
https://fizzy.cc/use-github-repo-to-host-images/

* "Anfora ... a decentralized social network to share photos."
https://github.com/anforaProject/anfora

* "Instead is a privacy-focused photo sharing service. ... not even the owner of the server can see posts."
https://github.com/danielbrauer/instead

* "Storing Images and Demos in your Repo"
Storing-Images-On-Github.md
https://gist.github.com/joncardasis/e6494afd538a400722545163eb2e1fa5
describes how to put images in a separate branch in a repo
for use in the main branch's README.
(But why would you do that instead of simply
using a completely separate repo?)

* "How to share images in GitHub from local system... upload my screenshots in GitHub"
https://www.edureka.co/community/68566/how-to-share-images-in-github-from-local-system


# changelog

2023-05-24: started by David Cary



