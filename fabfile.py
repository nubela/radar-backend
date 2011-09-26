from fabric.api import *
from time import sleep

env.hosts = ['root@ec2-75-101-174-29.compute-1.amazonaws.com']

def commit():
    local("git add . -A")
    local("git commit -m 'FabCommit'")

def deploy():
    local("git push dropbox-repo master")
    print "Sleeping for dropbox to sync..."
    sleep(10)
    print "Rebasing..."
    with cd("/home/nubela/Workspace/radar-backend"):
        run("git stash;git pull --rebase;git stash apply")
        run("/etc/init.d/apache2 restart")
    print "Done!"