def chilog(msg):
    f = open("debug.txt", "a+")
    f.write(msg)
    f.close()