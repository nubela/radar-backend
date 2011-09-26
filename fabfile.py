from fabric.api import *

env.hosts = ['root@ec2-75-101-174-29.compute-1.amazonaws.com']

def deploy():
    with cd("/home/nubela/Workspace/radar-backend"):
        run("git stash;git pull --rebase;git stash apply")
        run("/etc/init.d/apache2 restart")