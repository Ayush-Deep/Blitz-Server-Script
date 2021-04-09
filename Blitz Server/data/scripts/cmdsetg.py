import bs

def sB(val):
    if val == 0:
        with open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py") as (file):
            s = [ row for row in file ]
            s[14] = "shieldBomb = False"+"\n"
            f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py","w")
            for i in s:
                f.write(i)
            f.close()
            bs.screenMessage("ShieldBomb Set To False",color = (1,0,0))
    elif val == 1:
    	with open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py") as (file):
            s = [ row for row in file ]
            s[14] = "shieldBomb = True"+"\n"
            f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py","w")
            for i in s:
                f.write(i)
            f.close()
            bs.screenMessage("ShieldBomb Set To True",color =(0,1,0))

def bL(val):
    if val == 0:
        with open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py") as (file):
            s = [ row for row in file ]
            s[16] = "bombLights = False"+"\n"
            f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py","w")
            for i in s:
                f.write(i)
            f.close()
            bs.screenMessage("BombLight Set To False",color = (1,0,0))
    elif val == 1:
    	with open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py") as (file):
            s = [ row for row in file ]
            s[16] = "bombLights = True"+"\n"
            f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py","w")
            for i in s:
                f.write(i)
            f.close()
            bs.screenMessage("BombLights Set To True",color = (0,1,0))

def bN(val):
    if val == 0:
        with open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py") as (file):
            s = [ row for row in file ]
            s[18] = "bombName = False"+"\n"
            f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py","w")
            for i in s:
                f.write(i)
            f.close()
            bs.screenMessage("BombName Set To False",color = (1,0,0))
    elif val == 1:
    	with open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py") as (file):
            s = [ row for row in file ]
            s[18] = "bombName = True"+"\n"
            f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py","w")
            for i in s:
                f.write(i)
            f.close()
            bs.screenMessage("BombName Set To True",color = (0,1,0))

def bB(val):
    if val == 0:
        with open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py") as (file):
            s = [ row for row in file ]
            s[18] = "bigBomb = False"+"\n"
            f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py","w")
            for i in s:
                f.write(i)
            f.close()
            bs.screenMessage("BigBomb Set To False",color = (1,0,0))
    elif val == 1:
    	with open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py") as (file):
            s = [ row for row in file ]
            s[18] = "bigBomb = True"+"\n"
            f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py","w")
            for i in s:
                f.write(i)
            f.close()
            bs.screenMessage("BigBomb Set To True",color = (0,1,0))

def tN(Name1,Name2):
    N1 = "'"+Name1+"'"
    N2 = "'"+Name2+"'"
    with open(bs.getEnvironment()['systemScriptsDirectory'] + "/bsTeamGame.py") as (file):
        s = [ row for row in file ]
        s[10] = "gDefaultTeamNames = ("+N1+","+N2+")"+"\n"
        f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/bsTeamGame.py","w")
        for i in s:
            f.write(i)
        f.close()
        bs.screenMessage("Team Name Changed To("+Name1+","+Name2+")")

