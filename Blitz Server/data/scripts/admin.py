# -*- coding: utf-8 -*-
import bs
import bsUtils
import weakref
import random
import math
import time
import base64
import os,json
import bsInternal
import getPermissionsHashes as gph
from thread import start_new_thread
#from VirtualHost import DB_Handler,Language,MainSettings,_execSimpleExpression
import bsSpaz
from bsSpaz import _BombDiedMessage,_CurseExplodeMessage,_PickupMessage,_PunchHitMessage,gBasePunchCooldown,gBasePunchPowerScale,gPowerupWearOffTime,PlayerSpazDeathMessage,PlayerSpazHurtMessage
#from codecs import BOM_UTF8
import settings


class PermissionEffect(object):
    def __init__(self, position=(0, 1, 0), owner=None, prefix='ADMIN', prefixColor=(1, 1, 1),
                 prefixAnim=None, prefixAnimate=True,type = 1):
        if prefixAnim is None:
            prefixAnim = {0: (1, 1, 1), 500: (0.5, 0.5, 0.5)}
        self.position = position
        self.owner = owner

        # nick
        # text
        # color
        # anim
        # animCurve
        # particles


        # prefix
        if type == 1:
            m = bs.newNode('math', owner=self.owner, attrs={'input1': (0, 1.80, 0), 'operation': 'add'})
        else:
            m = bs.newNode('math', owner=self.owner, attrs={'input1': (0, 1.50, 0), 'operation': 'add'})
        self.owner.connectAttr('position', m, 'input2')

        self._Text = bs.newNode('text',
                                owner=self.owner,
                                attrs={'text': prefix,  # prefix text
                                       'inWorld': True,
                                       'shadow': 1.2,
                                       'flatness': 1.0,
                                       'color': prefixColor,
                                       'scale': 0.0,
                                       'hAlign': 'center'})

        m.connectAttr('output', self._Text, 'position')

        bs.animate(self._Text, 'scale', {0: 0.0, 1000: 0.01})  # smooth prefix spawn

        # animate prefix
        if prefixAnimate:
            bsUtils.animateArray(self._Text, 'color', 3, prefixAnim, True)  # animate prefix color

class SurroundBallFactory(object):
    def __init__(self):
        self.bonesTex = bs.getTexture("powerupCurse")
        self.bonesModel = bs.getModel("bonesHead")
        self.bearTex = bs.getTexture("bearColor")
        self.bearModel = bs.getModel("bearHead")
        self.aliTex = bs.getTexture("aliColor")
        self.aliModel = bs.getModel("aliHead")
        self.b9000Tex = bs.getTexture("cyborgColor")
        self.b9000Model = bs.getModel("cyborgHead")
        self.frostyTex = bs.getTexture("frostyColor")
        self.frostyModel = bs.getModel("frostyHead")
        self.cubeTex = bs.getTexture("crossOutMask")
        self.cubeModel = bs.getModel("powerup")
        try:
            self.mikuModel = bs.getModel("operaSingerHead")
            self.mikuTex = bs.getTexture("operaSingerColor")
        except:bs.PrintException()


        self.ballMaterial = bs.Material()
        self.impactSound = bs.getSound("impactMedium")
        self.ballMaterial.addActions(actions=("modifyNodeCollision", "collide", False))


class SurroundBall(bs.Actor):
    def __init__(self, spaz, shape="bones"):
        if spaz is None or not spaz.isAlive():
            return

        bs.Actor.__init__(self)

        self.spazRef = weakref.ref(spaz)

        factory = self.getFactory()

        s_model, s_texture = {
            "bones": (factory.bonesModel, factory.bonesTex),
            "bear": (factory.bearModel, factory.bearTex),
            "ali": (factory.aliModel, factory.aliTex),
            "b9000": (factory.b9000Model, factory.b9000Tex),
            "miku": (factory.mikuModel, factory.mikuTex),
            "frosty": (factory.frostyModel, factory.frostyTex),
            "RedCube": (factory.cubeModel, factory.cubeTex)
        }.get(shape, (factory.bonesModel, factory.bonesTex))

        self.node = bs.newNode("prop",
                               attrs={"model": s_model,
                                      "body": "sphere",
                                      "colorTexture": s_texture,
                                      "reflection": "soft",
                                      "modelScale": 0.5,
                                      "bodyScale": 0.1,
                                      "density": 0.1,
                                      "reflectionScale": [0.15],
                                      "shadowSize": 0.6,
                                      "position": spaz.node.position,
                                      "velocity": (0, 0, 0),
                                      "materials": [bs.getSharedObject("objectMaterial"), factory.ballMaterial]
                                      },
                               delegate=self)

        self.surroundTimer = None
        self.surroundRadius = 1.0
        self.angleDelta = math.pi / 12.0
        self.curAngle = random.random() * math.pi * 2.0
        self.curHeight = 0.0
        self.curHeightDir = 1
        self.heightDelta = 0.2
        self.heightMax = 1.0
        self.heightMin = 0.1
        self.initTimer(spaz.node.position)

    def getTargetPosition(self, spazPos):
        p = spazPos
        pt = (p[0] + self.surroundRadius * math.cos(self.curAngle),
              p[1] + self.curHeight,
              p[2] + self.surroundRadius * math.sin(self.curAngle))
        self.curAngle += self.angleDelta
        self.curHeight += self.heightDelta * self.curHeightDir
        if self.curHeight > self.heightMax or self.curHeight < self.heightMin:
            self.curHeightDir = -self.curHeightDir

        return pt

    def initTimer(self, p):
        self.node.position = self.getTargetPosition(p)
        self.surroundTimer = bs.Timer(30, bs.WeakCall(self.circleMove), repeat=True)

    def circleMove(self):
        spaz = self.spazRef()
        if spaz is None or not spaz.isAlive() or not spaz.node.exists():
            self.handleMessage(bs.DieMessage())
            return
        p = spaz.node.position
        pt = self.getTargetPosition(p)
        pn = self.node.position
        d = [pt[0] - pn[0], pt[1] - pn[1], pt[2] - pn[2]]
        speed = self.getMaxSpeedByDir(d)
        self.node.velocity = speed

    @staticmethod
    def getMaxSpeedByDir(direction):
        k = 7.0 / max((abs(x) for x in direction))
        return tuple(x * k for x in direction)

    def handleMessage(self, m):
        bs.Actor.handleMessage(self, m)
        if isinstance(m, bs.DieMessage):
            if self.surroundTimer is not None:
                self.surroundTimer = None
            self.node.delete()
        elif isinstance(m, bs.OutOfBoundsMessage):
            self.handleMessage(bs.DieMessage())

    def getFactory(cls):
        activity = bs.getActivity()
        if activity is None: raise Exception("no current activity")
        try:
            return activity._sharedSurroundBallFactory
        except Exception:
            f = activity._sharedSurroundBallFactory = SurroundBallFactory()
            return f


class Enhancement(bs.Actor):
    def __init__(self, spaz, player):
        bs.Actor.__init__(self)
        self.sourcePlayer = player
        self.spazRef = weakref.ref(spaz)
        self.spazNormalColor = spaz.node.color
        self.Decorations = []
        self.Enhancements = []
        self._powerScale = 1.0
        self._armorScale = 1.0
        self._lifeDrainScale = None
        self._damageBounceScale = None
        self._remoteMagicDamge = False
        self._MulitPunch = None
        self._AntiFreeze = 1.0
        self.fallWings = 0
        
        self.checkDeadTimer = None
        self._hasDead = False
        self.light = None

	flag = 0
        profiles = []
        profiles = self.sourcePlayer.getInputDevice()._getPlayerProfiles()  


	cl_str = self.sourcePlayer.get_account_id()
	clID = self.sourcePlayer.getInputDevice().getClientID()
	#print cl_str, clID

        if profiles == [] or profiles == {}:
            profiles = bs.getConfig()['Player Profiles']

	def getTag(*args):
		  #if alreadyHasTag: return True
		  #profiles = self._player.getInputDevice()._getPlayerProfiles()
		  for p in profiles:
		    if '/tag' in p:
		     try:
			      tag = p.split(' ')[1]
			      if '\\' in tag:
				#print tag + ' before'
				tag =tag.replace('\d','\ue048'.decode('unicode-escape'))
				tag =tag.replace('\c','\ue043'.decode('unicode-escape'))
				tag =tag.replace('\h','\ue049'.decode('unicode-escape'))
				tag =tag.replace('\s','\ue046'.decode('unicode-escape'))
				tag =tag.replace('\\n','\ue04b'.decode('unicode-escape'))
				tag =tag.replace('\\f','\ue04f'.decode('unicode-escape'))
			      	#print tag + ' after'		
			      return tag
		     except:
			pass   
		  return '0'

        try:
		if cl_str in gph.effectCustomers:
			effect = gph.effectCustomers[cl_str]["effect"]
			if effect == 'ice':
				self.snowTimer = bs.Timer(500, bs.WeakCall(self.emitIce), repeat=True)
			elif effect == 'sweat':
				self.smokeTimer = bs.Timer(40, bs.WeakCall(self.emitSmoke), repeat=True)
			elif effect == 'scorch':
				self.scorchTimer = bs.Timer(500, bs.WeakCall(self.update_Scorch), repeat=True)
			elif effect == 'glow':
				self.addLightColor((1, 0.6, 0.4));self.checkDeadTimer = bs.Timer(150, bs.WeakCall(self.checkPlayerifDead), repeat=True)
			elif effect == 'distortion':
				self.DistortionTimer = bs.Timer(1000, bs.WeakCall(self.emitDistortion), repeat=True)
			elif effect == 'slime':
				self.slimeTimer = bs.Timer(250, bs.WeakCall(self.emitSlime), repeat=True)
			elif effect == 'metal':
				self.metalTimer = bs.Timer(500, bs.WeakCall(self.emitMetal), repeat=True)
			elif effect == 'surrounder':
				self.surround = SurroundBall(spaz, shape="bones")
                elif cl_str in gph.surroundingObjectEffect:
		    self.surround = SurroundBall(spaz, shape="bones")
		    flag = 1
                elif cl_str in gph.sparkEffect:
                    self.sparkTimer = bs.Timer(100, bs.WeakCall(self.emitSpark), repeat=True)
		    flag = 1
                elif cl_str in gph.smokeEffect:
		    self.smokeTimer = bs.Timer(40, bs.WeakCall(self.emitSmoke), repeat=True)
		    flag = 1
                elif cl_str in gph.scorchEffect:
		    self.scorchTimer = bs.Timer(500, bs.WeakCall(self.update_Scorch), repeat=True)
		    flag = 1
                elif cl_str in gph.distortionEffect:
		    self.DistortionTimer = bs.Timer(1000, bs.WeakCall(self.emitDistortion), repeat=True)
		    flag = 1
                elif cl_str in gph.glowEffect:
		    self.addLightColor((1, 0.6, 0.4));self.checkDeadTimer = bs.Timer(150, bs.WeakCall(self.checkPlayerifDead), repeat=True)
		    flag = 1
                elif cl_str in gph.iceEffect:
		    self.snowTimer = bs.Timer(500, bs.WeakCall(self.emitIce), repeat=True)
		    flag = 1
                elif cl_str in gph.slimeEffect:
		    self.slimeTimer = bs.Timer(250, bs.WeakCall(self.emitSlime), repeat=True)
		    flag = 1
                elif cl_str in gph.metalEffect:
		    self.metalTimer = bs.Timer(500, bs.WeakCall(self.emitMetal), repeat=True)
		    flag = 1
	
		if cl_str in gph.customlist:
			    PermissionEffect(owner = spaz.node,prefix =gph.customlist[cl_str],prefixAnim = {0: (1,0,0), 250: (0,1,0),250*2:(0,0,1),250*3:(1,0,0)})
                elif cl_str in gph.customtagHashes  or cl_str in gph.topperslist:
			    tag = getTag(1)
			    if tag == '0': tag = u'\ue047M3mBeR\ue047'
			    PermissionEffect(owner = spaz.node,prefix = tag,prefixAnim = {0: (1,0,0), 250: (0,1,0),250*2:(0,0,1),250*3:(1,0,0)})
                elif cl_str in gph.ownerHashes:
			    tag = getTag(1)
			    if tag == '0': tag = u'\ue048O|W|N|E|R\ue048'
			    PermissionEffect(owner = spaz.node,prefix = tag,prefixAnim = {0: (1,0,0), 250: (0,1,0),250*2:(0,0,1),250*3:(1,0,0)})
                elif cl_str in gph.adminHashes:
			    tag = getTag(1)
			    if tag == '0': tag = u'\ue04cA.D.M.I.N\ue04c'
			    PermissionEffect(owner = spaz.node,prefix = tag,prefixAnim = {0: (1,0,0), 250: (0,1,0),250*2:(0,0,1),250*3:(1,0,0)})
                elif cl_str in gph.vipHashes:	
			    tag = getTag(1)
			    if tag == '0': tag = u'[V.I.P+]'
			    PermissionEffect(owner = spaz.node,prefix = tag,prefixAnim = {0: (1,0,0), 250: (0,1,0),250*2:(0,0,1),250*3:(1,0,0)})
        except:
                pass

	if settings.enableStats:

	    if os.path.exists(bs.getEnvironment()['systemScriptsDirectory'] + "/pStats.json"):
		f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/pStats.json", "r")
		#pats = json.loads(f.read())
		aid = str(self.sourcePlayer.get_account_id())
		pats = {}
		try:
		    pats = json.loads(f.read())	
		except Exception:
		    bs.printException()
		if aid in pats:
		    rank = pats[aid]["rank"]
		    kill = pats[aid]["kills"]
		    death = pats[aid]["deaths"]
		    if int(rank) < 6:
			#dragon='' crown= fireball=	ninja= skull=	
			if rank == '1':
				icon = '' #crown
				if flag == 0 and settings.enableTop5effects: self.neroLightTimer = bs.Timer(500, bs.WeakCall(self.neonLightSwitch,("shine" in self.Decorations),("extra_Highlight" in self.Decorations),("extra_NameColor" in self.Decorations)),repeat = True)
			elif rank == '2': 
				icon = '' #dragon
				if flag ==0 and settings.enableTop5effects: self.smokeTimer = bs.Timer(40, bs.WeakCall(self.emitSmoke), repeat=True)
			elif rank == '3': 
				icon ='' #helmet'
				if flag == 0 and settings.enableTop5effects: self.addLightColor((1, 0.6, 0.4));self.scorchTimer = bs.Timer(500, bs.WeakCall(self.update_Scorch), repeat=True)
			elif rank == '4': 
				icon = '' #fireball
				if flag ==0 and settings.enableTop5effects: self.metalTimer = bs.Timer(500, bs.WeakCall(self.emitMetal), repeat=True)

			else: 
				icon = '' #bull head  
				if flag==0 and settings.enableTop5effects: self.addLightColor((1, 0.6, 0.4));self.checkDeadTimer = bs.Timer(150, bs.WeakCall(self.checkPlayerifDead), repeat=True)
			display = icon + '#' + str(rank) +icon
		        PermissionEffect(owner = spaz.node,prefix = display,prefixAnim = {0: (1,1,1)},type = 2)
		    else:
			display = '#' + str(rank)
		        PermissionEffect(owner=spaz.node, prefix=u'«\U000026C4»|' + str(pats[str(player.get_account_id())]["rank"]),
		                     prefixAnim={0: (1,1,1)},type=2)
	

        if "smoke" and "spark" and "snowDrops" and "slimeDrops" and "metalDrops" and "Distortion" and "neroLight" and "scorch" and "HealTimer" and "KamikazeCheck" not in self.Decorations:
            #self.checkDeadTimer = bs.Timer(150, bs.WeakCall(self.checkPlayerifDead), repeat=True)

            if self.sourcePlayer.isAlive() and isinstance(self.sourcePlayer.actor,bs.PlayerSpaz) and self.sourcePlayer.actor.node.exists():
                #print("OK")
                self.sourcePlayer.actor.node.addDeathAction(bs.Call(self.handleMessage,bs.DieMessage()))


    def checkPlayerifDead(self):
        spaz = self.spazRef()
        if spaz is None or not spaz.isAlive() or not spaz.node.exists():
            self.checkDeadTimer = None
            self.handleMessage(bs.DieMessage())
            return
    def update_Scorch(self):
        spaz = self.spazRef()
        if spaz is not None and spaz.isAlive() and spaz.node.exists():
            color = (random.random(),random.random(),random.random())
            if not hasattr(self,"scorchNode") or self.scorchNode == None:
                self.scorchNode = None
                self.scorchNode = bs.newNode("scorch",attrs={"position":(spaz.node.position),"size":1.17,"big":True})
                spaz.node.connectAttr("position",self.scorchNode,"position")
            bsUtils.animateArray(self.scorchNode,"color",3,{0:self.scorchNode.color,500:color})
        else:
            self.scorchTimer = None
            self.scorchNode.delete()
            self.handleMessage(bs.DieMessage())
        
    def neonLightSwitch(self,shine,Highlight,NameColor):
        spaz = self.spazRef()
        if spaz is not None and spaz.isAlive() and spaz.node.exists():
            color = (random.random(),random.random(),random.random())
            if NameColor:
                bsUtils.animateArray(spaz.node,"nameColor",3,{0:spaz.node.nameColor,500:bs.getSafeColor(color)})
            if shine:color = tuple([min(10., 10 * x) for x in color])
            bsUtils.animateArray(spaz.node,"color",3,{0:spaz.node.color,500:color})
            if Highlight:
                #print spaz.node.highlight
                color = (random.random(),random.random(),random.random())
                if shine:color = tuple([min(10., 10 * x) for x in color])
                bsUtils.animateArray(spaz.node,"highlight",3,{0:spaz.node.highlight,500:color})
        else:
            self.neroLightTimer = None
            self.handleMessage(bs.DieMessage())

 
    def addLightColor(self, color):
        self.light = bs.newNode("light", attrs={"color": color,
                                                "heightAttenuated": False,
                                                "radius": 0.4})
        self.spazRef().node.connectAttr("position", self.light, "position")
        bsUtils.animate(self.light, "intensity", {0: 0.1, 250: 0.3, 500: 0.1}, loop=True)
        
    def emitDistortion(self):
        spaz = self.spazRef()
        if spaz is None or not spaz.isAlive() or not spaz.node.exists():
            self.handleMessage(bs.DieMessage())
            return
        bs.emitBGDynamics(position=spaz.node.position,emitType="distortion",spread=1.0)
        bs.emitBGDynamics(position=spaz.node.position, velocity=spaz.node.velocity,count=random.randint(1,5),emitType="tendrils",tendrilType="smoke")

        
    def emitSpark(self):
        spaz = self.spazRef()
        if spaz is None or not spaz.isAlive() or not spaz.node.exists():
            self.handleMessage(bs.DieMessage())
            return
        bs.emitBGDynamics(position=spaz.node.position, velocity=spaz.node.velocity, count=random.randint(1,10), scale=2, spread=0.2,
                          chunkType="spark")
    def emitIce(self):
        spaz = self.spazRef()
        if spaz is None or not spaz.isAlive() or not spaz.node.exists():
            self.handleMessage(bs.DieMessage())
            return
        bs.emitBGDynamics(position=spaz.node.position , velocity=spaz.node.velocity, count=random.randint(2,8), scale=0.4, spread=0.2,
                          chunkType="ice")
    def emitSmoke(self):
        spaz = self.spazRef()
        if spaz is None or not spaz.isAlive() or not spaz.node.exists():
            self.handleMessage(bs.DieMessage())
            return
        bs.emitBGDynamics(position=spaz.node.position, velocity=spaz.node.velocity, count=random.randint(1,10), scale=2, spread=0.2,
                          chunkType="sweat")
    def emitSlime(self):
        spaz = self.spazRef()
        if spaz is None or not spaz.isAlive() or not spaz.node.exists():
            self.handleMessage(bs.DieMessage())
            return
        bs.emitBGDynamics(position=spaz.node.position , velocity=spaz.node.velocity, count=random.randint(1,10), scale=0.4, spread=0.2,
                          chunkType="slime")
    def emitMetal(self):
        spaz = self.spazRef()
        if spaz is None or not spaz.isAlive() or not spaz.node.exists():
            self.handleMessage(bs.DieMessage())
            return
        bs.emitBGDynamics(position=spaz.node.position, velocity=spaz.node.velocity, count=random.randint(2,8), scale=0.4, spread=0.2,
                          chunkType="metal")
    def handleMessage(self, m):
        #self._handleMessageSanityCheck()
        
        if isinstance(m, bs.OutOfBoundsMessage):
            self.handleMessage(bs.DieMessage())
        elif isinstance(m, bs.DieMessage):
            if hasattr(self,"light") and self.light is not None:self.light.delete()
            if hasattr(self,"smokeTimer"):self.smokeTimer = None
            if hasattr(self,"surround"):self.surround = None
            if hasattr(self,"sparkTimer"):self.sparkTimer = None
            if hasattr(self,"snowTimer"):self.snowTimer = None
            if hasattr(self,"metalTimer"):self.metalTimer = None
            if hasattr(self,"DistortionTimer"):self.DistortionTimer = None
            if hasattr(self,"slimeTimer"):self.slimeTimer = None
            if hasattr(self,"KamikazeCheck"):self.KamikazeCheck = None
            if hasattr(self,"neroLightTimer"):self.neroLightTimer = None
            if hasattr(self,"checkDeadTimer"):self.checkDeadTimer = None
            if hasattr(self,"HealTimer"):self.HealTimer = None
            if hasattr(self,"scorchTimer"):self.scorchTimer = None
            if hasattr(self,"scorchNode"):self.scorchNode = None
            if not self._hasDead:
                spaz = self.spazRef()
                #print str(spaz) + "Spaz"
                if spaz is not None and spaz.isAlive() and spaz.node.exists():
                    spaz.node.color = self.spazNormalColor
                killer = spaz.lastPlayerAttackedBy if spaz is not None else None
                try:
                    if killer in (None,bs.Player(None)) or killer.actor is None or not killer.actor.exists() or killer.actor.hitPoints <= 0:killer = None
                except:killer = None
                #if hasattr(self,"hasDead") and not self.hasDead:
                
                self._hasDead = True
            
        bs.Actor.handleMessage(self, m)


def _Modify_BS_PlayerSpaz__init__(self, color=(1, 1, 1), highlight=(0.5, 0.5, 0.5), character="Spaz", player=None,
                           powerupsExpire=True):
    if player is None: player = bs.Player(None)

    bsSpaz.Spaz.__init__(self, color=color, highlight=highlight, character=character, sourcePlayer=player,
                     startInvincible=True, powerupsExpire=powerupsExpire)
    self.lastPlayerAttackedBy = None  # FIXME - should use empty player ref
    self.lastAttackedTime = 0
    self.lastAttackedType = None
    self.heldCount = 0
    self.lastPlayerHeldBy = None  # FIXME - should use empty player ref here
    self._player = player

    # grab the node for this player and wire it to follow our spaz (so players" controllers know where to draw their guides, etc)
    if player.exists():
        playerNode = bs.getActivity()._getPlayerNode(player)
        self.node.connectAttr("torsoPosition", playerNode, "position")
    
    self.HasEnhanced = False
    self.Enhancement = Enhancement(self, self.sourcePlayer).autoRetain()

bsSpaz.PlayerSpaz.__init__ = _Modify_BS_PlayerSpaz__init__



