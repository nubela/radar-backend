#!/usr/bin/python
from flup.server.fcgi import WSGIServer
from radar import app

if __name__ == '__main__':
    WSGIServer(app, bindAddress='/home/nubela/fcgi.sock').run()