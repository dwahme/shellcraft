
def chilog(msg):
    f = open("log.txt", "a+")
    f.write(msg + "\n")
    f.close()
