from fabric.api import *
from time import sleep

env.hosts = ['root@ec2-75-101-174-29.compute-1.amazonaws.com']

def error():
    with cd("/home/nubela/Workspace/radar-backend"):
        run("tail error.log")
    with cd("/var/log/apache2"):
        run("tail error.log")

def deploy():
    with cd("/home/nubela/Workspace/radar-backend"):
        run("git pull --rebase")
        run("/etc/init.d/apache2 restart")
    print "Done!"
