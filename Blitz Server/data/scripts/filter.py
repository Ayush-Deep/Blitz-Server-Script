import bs

f_words = ["mc","bc","fuck","bsdk"]

def warn(clientID):
    bs.screenMessage("Warning!!! Do Not Misbehave", color = (1,0,0), transient=True, clients=[clientID])