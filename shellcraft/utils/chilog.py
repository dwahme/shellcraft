def chilog(msg):
    f = open("debug.txt", "w")
    f.write(msg)
    f.close()