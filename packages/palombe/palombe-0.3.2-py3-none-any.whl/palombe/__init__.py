import os

def __mkfifo(name):
    prefix = "/tmp/palombe/"
    path = "%s%s" % (prefix, name)
    if not os.path.exists(prefix):
        os.makedirs(prefix)
    if not os.path.exists(path):
        os.mkfifo(path, 0o600)
    return path

def send(name, value):
    file = open(__mkfifo(name), "w")
    file.write(value)

def receive(name):
    path = __mkfifo(name)
    file = open(path, "r")
    os.remove(path)
    return file.read()
