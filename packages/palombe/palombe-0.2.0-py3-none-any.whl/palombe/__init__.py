import os

PREFIX = "/tmp/palombe/"

def send(name, value):
    path = "%s%s" % (PREFIX, name)
    os.makedirs(PREFIX)
    os.mkfifo(path)
    file = open(path, "w")
    file.write(value)

def receive(name):
    path = "%s%s" % (PREFIX, name)
    file = open(path, "r") 
    return file.read()
