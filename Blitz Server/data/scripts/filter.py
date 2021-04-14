import bs
import bsInternal
f_words = ["mc","bc","fuck","bsdk"]

warndict = {}

def k(cid):
	if cid in warndict:
		print(warndict,"Yes")
	else:
		warndict.update({cid:0})

def check(cid):
	global warndict
	if warndict[cid] == 1:
			#bsInternal._disconnectClient(str(cid))
		bsInternal._disconnectClient(int(cid))
		bs.screenMessage("Kicking For Misbehave", color = (1,0,0))
		warndict.pop(cid)
	elif warndict[cid] == 0:
		warndict[cid] = 1

def warn(clientID):
    bs.screenMessage("Warning!!! Do Not Misbehave", color = (1,0,0), transient=True, clients=[clientID])
    if warndict[clientID] == 0:
    	bs.screenMessage("Last Chance Warning 1/2", color = (1,0,0), transient=True, clients=[clientID])
