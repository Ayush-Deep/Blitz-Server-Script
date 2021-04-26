import bs
from bsSpaz import *
import bsInternal
import getPermissionsHashes as gph
import perkid

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

def damage(pbid):
    old = perkid.damage
    new = old.append(pbid)
    with open(bs.getEnvironment()['systemScriptsDirectory'] + "/perkid.py") as (file):
        s = [ row for row in file ]
        s[0] = "damage = "+str(new)+"\n"
        f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/perkid.py","w")
        for i in s:
            f.write(i)
        f.close()
        bs.screenMessage("You Get Damage Boost Of +0.05",color = (0,1,0))

def heal(pbid):
    old = perkid.heal
    new = old.append(pbid)
    with open(bs.getEnvironment()['systemScriptsDirectory'] + "/perkid.py") as (file):
        s = [ row for row in file ]
        s[1] = "heal = "+str(new)+"\n"
        f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/perkid.py","w")
        for i in s:
            f.write(i)
        f.close()
        bs.screenMessage("You Get Healing Of +50 Health If Health Below 40%",color = (0,1,0))

def health(pbid):
    old = perkid.healthpo
    new = old.append(pbid)
    with open(bs.getEnvironment()['systemScriptsDirectory'] + "/perkid.py") as (file):
        s = [ row for row in file ]
        s[2] = "healthpo = "+str(new)+"\n"
        f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/perkid.py","w")
        for i in s:
            f.write(i)
        f.close()
        bs.screenMessage("You Get Health Of +250 Extra Health",color = (0,1,0))


oldInit = PlayerSpaz.__init__

def newInit(self, *args, **kwargs):
    oldInit(self, *args, **kwargs)

    def punch():
        if self.getPlayer().get_account_id() in perkid.damage or self.getPlayer().get_account_id() in gph.ownerHashes:
            self._punchPowerScale = 1.25
    bs.gameTimer(300,bs.Call(punch))

    def hel():
        if self.getPlayer().get_account_id() in perkid.damage or self.getPlayer().get_account_id() in gph.ownerHashes:
            if self.hitPoints <= 400:
                self.hitPoints+= 50
    bs.gameTimer(2000,bs.Call(hel),repeat=True)

    def healh():
        if self.getPlayer().get_account_id() in perkid.damage or self.getPlayer().get_account_id() in gph.ownerHashes:
            self.hitPointsMax = 1250
    bs.gameTimer(300,bs.Call(healh))
    '''def boxer(val,n):
        if self.getPlayer().get_account_id() in gph.ownerHashes:
            if self.node.boxingGloves != 0 and n != 2:
                print("Yooooooooooooo")
            elif n == 2:
                if val:
                    self._hasBoxingGloves = True
                    self.equipBoxingGloves()
                else:
                    self._hasBoxingGloves = False
                    self.node.boxingGloves = 0
                punch()
    bs.gameTimer(500,bs.Call(boxer,True,2))
    bs.gameTimer(5000,bs.Call(boxer,False,2))'''

PlayerSpaz.__init__ = newInit
