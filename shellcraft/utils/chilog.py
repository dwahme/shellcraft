
def chilog(msg):
    f = open("log.txt", "a+")
    f.write(msg)
    f.close()
