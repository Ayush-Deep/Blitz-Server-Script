#Characters effects v1.0
#Maded by Froshlee14

from bsUI import *
import random, bs, bsUtils, bsUI
from bsSpaz import PlayerSpaz,Spaz, PlayerSpazDeathMessage
from bsUI import PlayerProfilesWindow, gMedUI, gSmallUI,PopupWindow,gDoAndroidNav,gTitleColor

def getDefaultSettings():
    newConfig = {"effect":'none',
			"spawnEffect":'in',
			"deathEffect":'fly',
            "tab":'info',
            "color":True,
            }
    return newConfig
	
if "effectsMod" in bs.getConfig():
    oldConfig = bs.getConfig()["effectsMod"]
    for setting in getDefaultSettings():
        if setting not in oldConfig:
            bs.getConfig()["effectsMod"] = getDefaultSettings()
else:
    bs.getConfig()["effectsMod"] = getDefaultSettings()
bs.writeConfig()

oldWindowInit = PlayerProfilesWindow.__init__
def newWindowInit(self, *args, **kwargs):
    oldWindowInit(self, *args, **kwargs)
    width = 600 if gSmallUI else 550
    xInset = 50 if gSmallUI else 0
    height = 360 if gSmallUI else 385 if gMedUI else 410
	
    def doMenu():
        bs.containerWidget(edit=self._rootWidget,transition=self._transitionOut)
        EffectsMenu()
		
    self._effectsModButton = bs.buttonWidget(parent=self._rootWidget, autoSelect=True,
                                            position=(width-80,self._height-60), size=(50,50),
                                            scale=0.8, textScale=1.5,textColor=(1,1,0),label=None,
                                            onActivateCall=doMenu,color= (0.1, 0.1, 1),iconScale=1.25,
                                            icon=bs.getTexture("cuteSpaz"),buttonType="square")
											
PlayerProfilesWindow.__init__ = newWindowInit

class EffectsMenu(PopupWindow):

    def __init__(self,transition='inRight'):
        self._width = width = 550
        self._height = height = 420

        self._scrollWidth = self._width*0.90
        self._scrollHeight = self._height - 180
        self._subWidth = self._scrollWidth*0.95;
        self._subHeight = 200

        self._current_tab = bs.getConfig()['effectsMod']['tab']
		
        txtFinal = "Ajustes de Effects Mod" if bs.getLanguage() == "Spanish" else "Effects Mod Settings"
		
        if bs.getLanguage() == "Spanish":
            self._credits = ("Modifica y aplica efectos\n"
           	                "personalizados a tus personajes.\n\n"
                            "Programado por Froshlee14")
        else:
            self._credits = ("Modify and add custom\n"
           	                "effects to your characters.\n\n"
                            "Mod made by SAHIL")

        self._rootWidget = bs.containerWidget(size=(width,height),transition=transition,
                           scale=2.0 if gSmallUI else 1.4 if gMedUI else 1.0,
                           stackOffset=(0,-30) if gSmallUI else (0,0))
        
        self._backButton = b = bs.buttonWidget(parent=self._rootWidget,autoSelect=True,position=(60,self._height-75),size=(130,60),
                            scale=0.8,textScale=1.2,label=bs.Lstr(resource='backText'),buttonType='back',onActivateCall=self._back)	

        if gDoAndroidNav: bs.buttonWidget(edit=self._backButton,buttonType='backSmall',size=(60,60),label=bs.getSpecialChar('back'))
                                               
        bs.containerWidget(edit=self._rootWidget,cancelButton=b)
        t = bs.textWidget(parent=self._rootWidget,position=(0,height-70),size=(width,50),
                          text=txtFinal,  hAlign="center",color=gTitleColor, vAlign="center",maxWidth=width*0.5)
												
        v = self._subHeight - 55
        v0 = height - 90
     			
        tabs = [['general','General' if bs.getLanguage() == "Spanish" else 'General'],
                ['effects','Efectos' if bs.getLanguage() == "Spanish" else 'Effects'],
                #['soon','Proximamente' if bs.getLanguage() == "Spanish" else 'Coming soon'],
                ['info',"Info" if bs.getLanguage() == "Spanish" else 'Info'],]
			   
        self._tab_buttons = bsUI._createTabButtons(
            self._rootWidget, tabs,
            pos=(self._width*0.08,45+self._scrollHeight), 
            size=(self._scrollWidth*0.93,30),
            onSelectCall=self._setTab)	
			
        self._scrollWidget = bs.scrollWidget(parent=self._rootWidget,size=(self._subWidth,self._scrollHeight),
                                             highlight=False, position=(self._width*0.08,51),captureArrows=True)
        self._tabContainer = None
        self._setTab(self._current_tab)
		
    def _setTab(self,tab):
        self._colorTimer = None
        self._current_tab = tab
        bs.getConfig()['effectsMod']['tab'] = tab
        bs.writeConfig()
        bsUI._updateTabButtonColors(self._tab_buttons, tab)
        if self._tabContainer is not None and self._tabContainer.exists():
            self._tabContainer.delete()
        self._tabData = {}
		
        if tab == 'info':
            subHeight = 200
            self._tabContainer = c = bs.containerWidget(parent=self._scrollWidget,size=(self._subWidth,subHeight),
                                                background=False)
            bs.widget(edit=self._tabContainer,upWidget=self._backButton)
            v = subHeight - 40
            cWidth = self._scrollWidth
            cHeight = min(self._scrollHeight, 200*1.0+100)
            
            self._timeDelayText = bs.textWidget(
                parent=c, position=(0,v),
                color=(0.1, 1.0, 0.1),
                scale=1.2, size=(self._subWidth, 0),
                maxWidth=cWidth * 0.9, maxHeight=cHeight * 0.9, hAlign='center',
                vAlign='center', text='EFFECTS MOD v1.1')			
            v -= 100
            t = bs.textWidget(
                parent=c, position=(0, v),
                color=(0.8, 0.8, 0.8),
                scale=0.8, size=(self._subWidth*0.95, 0),
                maxWidth=cWidth * 0.9, maxHeight=cHeight * 0.9, hAlign='center',
                vAlign='center', text=self._credits)
            v -= 140

        elif tab == 'general':
            subHeight = 200
            self._tabContainer = c = bs.containerWidget(parent=self._scrollWidget,size=(self._subWidth,subHeight), background=False)
            v = subHeight - 70

            reset = bs.buttonWidget(parent=c, autoSelect=True,onActivateCall=self.restoreSettings,
                                    position=((self._scrollWidth*0.45)-150, v), size=(300,50),scale=1.0, textScale=1.2,textColor=(1,1,1),
                                    label="Restaurar ajustes por defecto" if bs.getLanguage() == "Spanish" else "Restore default settings")
            bs.buttonWidget(edit=reset,upWidget=self._backButton)
            v -= 70

            self.bw = bs.checkBoxWidget(parent=c,position=(self._subWidth*0.1,v), value=bs.getConfig()["effectsMod"]["color"],
                                      onValueChangeCall=bs.Call(self._setSetting,'color'), maxWidth=self._scrollWidth*0.9,
                                      text='Aplicar color de perfiles' if bs.getLanguage() == 'Spanish' else 'Apply profile colors',autoSelect=True)

        elif tab == "effects":
            self._selected = None

            baseScale = 2.4 if gSmallUI else 1.5 if gMedUI else 1.0
            popupMenuScale = baseScale*1.2
            subHeight = 250
            v = subHeight - 20

            self._tabContainer = c = bs.containerWidget(parent=self._rootWidget,size=(self._subWidth,subHeight),
                                                background=False)

            spawnEffectsList = ['none','in','out','xplode','show']
            if bs.getLanguage() == "Spanish": spawnEffectsListDisplay = ['Ninguno','Ondas adentro','Ondas afuera','Explosion','Mostrar circulo']
            else: spawnEffectsListDisplay = ['None','Circles In','Circles Out','Circle Explode','Show circle']
			  
            t = bs.textWidget(parent=c,position=(self._subWidth*0.2,v),
                          text="Efectos de spawn" if bs.getLanguage() == "Spanish" else "Spawn effects",
                          maxWidth=self._scrollWidth,size=(self._subWidth*0.5,self._scrollHeight*0.1),color=(0.7,0.7,0.7),hAlign="left",scale=0.8,)


            sePopup = PopupMenu(parent=c,position=(self._subWidth*0.6,v-15),width=150,scale=popupMenuScale,
                                  choices=spawnEffectsList,
                                  choicesDisplay=spawnEffectsListDisplay,
                                  currentChoice= bs.getConfig()["effectsMod"]["spawnEffect"],
                                  onValueChangeCall=self._setSpawnEffect)
            bs.widget(edit=sePopup.getButtonWidget(),upWidget=self._backButton)
            v -= 60

            effectsList = ['none','path','fire']
            if bs.getLanguage() == "Spanish": effectsListDisplay = ['Ninguno','Linea punteda','Hombre de fuego']
            else: effectsListDisplay = ['None','Dotted line','Fireman'] 
			  
            t = bs.textWidget(parent=c,position=(self._subWidth*0.2,v),
                          text="Efectos in-Game" if bs.getLanguage() == "Spanish" else "In-Game ffects",
                          maxWidth=self._scrollWidth,size=(self._subWidth*0.5,self._scrollHeight*0.1),color=(0.7,0.7,0.7),hAlign="left",scale=0.8,)


            ePopup = PopupMenu(parent=c,position=(self._subWidth*0.6,v-15),width=150,scale=popupMenuScale,
                                  choices=effectsList,
                                  choicesDisplay=effectsListDisplay,
                                  currentChoice= bs.getConfig()["effectsMod"]["effect"],
                                  onValueChangeCall=self._setEffect)
            v -= 60

            deathEffectsList = ['none','in','out','xplode','show','bones','fly','skull']
            if bs.getLanguage() == "Spanish": deathEffectsListDisplay = ['Ninguno','Ondas adentro','Ondas afuera','Explosion','Mostrar circulo','Huesos','Levitar','Calavera']
            else: deathEffectsListDisplay = ['None','Circles In','Circles Out','Circle Explode','Show cirlce ','Become bones','Levitate','Show Skull']
			  
            t = bs.textWidget(parent=c,position=(self._subWidth*0.2,v),
                          text="Efectos de muerte" if bs.getLanguage() == "Spanish" else "Death effects",
                          maxWidth=self._scrollWidth,size=(self._subWidth*0.5,self._scrollHeight*0.1),color=(0.7,0.7,0.7),hAlign="left",scale=0.8,)


            dePopup = PopupMenu(parent=c,position=(self._subWidth*0.6,v-15),width=150,scale=popupMenuScale,
                                  choices=deathEffectsList,
                                  choicesDisplay=deathEffectsListDisplay,
                                  currentChoice= bs.getConfig()["effectsMod"]["deathEffect"],
                                  onValueChangeCall=self._setDeathEffect)
            #self.updateProfiles((l*32)-20,(r*32)-20)
    def _setSpawnEffect(self,m):
        bs.getConfig()["effectsMod"]["spawnEffect"] = m
        bs.writeConfig()

    def _setEffect(self,m):
        bs.getConfig()["effectsMod"]["effect"] = m
        bs.writeConfig()

    def _setDeathEffect(self,m):
        bs.getConfig()["effectsMod"]["deathEffect"] = m
        bs.writeConfig()

    def _setSetting(self,setting,m):
        bs.getConfig()["effectsMod"][setting] =  False if m==0 else True
        bs.writeConfig()

    def restoreSettings(self):
        def doIt():
            bs.getConfig()["effectsMod"] = getDefaultSettings()
            bs.writeConfig()
            self._setTab("general")
            bs.screenMessage("Ajustes restaurados" if bs.getLanguage() == "Spanish" else "Settings restored")
        ConfirmWindow("Restaurar ajustes por defecto?" if bs.getLanguage() == "Spanish" else "Restore default settings?",
                          width=400, height=120, action=doIt, okText=bs.Lstr(resource='okText'))


    def _back(self):
        bs.containerWidget(edit=self._rootWidget,transition='outRight')
        self._colorTimer = None
        uiGlobals['mainMenuWindow'] = PlayerProfilesWindow(transition='inLeft').getRootWidget()

def doRing(self,type='in'):
        p = self.node.position
        pos = (p[0],p[1]-0.3,p[2])
        c = bs.getConfig()["effectsMod"]["color"]

        if type == 'in': do = False
        elif type == 'out': do = False
        elif type == 'xplode': do = True
        elif type == 'show':do = False
        else: do = True

        m = bs.newNode('math', owner=self.node, attrs={'input1': (0, 0, 0), 'operation': 'add'})
        self.node.connectAttr('position', m, 'input2')
        ring = bs.newNode('locator',attrs={'shape':'circleOutline','position':pos,
            'color':self.node.color if c else (5,5,5),'opacity':1,'drawBeauty':do,'additive':False,'size':[2]})
        m.connectAttr('output', ring, 'position')
				
        if type == 'in':
            time = 300
            bsUtils.animateArray(ring,'size',1,{0:[5],300:[0]})
            bs.animate(ring, 'opacity', {0:0, 160:1})

        elif type == 'out':
            time = 500
            bsUtils.animateArray(ring,'size',1,{0:[0],500:[4]})
            bs.animate(ring, 'opacity', {0:1, 500:0})
			
        elif type == 'xplode':
            time = 700
            bsUtils.animateArray(ring,'size',1,{0:[0],700:[100]})
            bs.animate(ring, 'opacity', {0:1, 600:0})
			
        elif type == 'show':
            time = 2000
            bsUtils.animateArray(ring,'size',1,{0:[0],200:[2.2],300:[1.8],1700:[1.8],1800:[2.2],2000:[0]})
            #bs.animate(ring, 'opacity', {0:1, 1800:0})

        else: time = 200

        bs.gameTimer(time,ring.delete)

def newPlayerSpazDeathMessageInit(self, spaz, wasKilled, killerPlayer, how):
        """
        Instantiate a message with the given values.
        """
        self.spaz = spaz
        self.killed = wasKilled
        self.killerPlayer = killerPlayer
        self.how = how

        deff = bs.getConfig()["effectsMod"]["deathEffect"]

        if deff == "none": pass
        elif deff == "bones":
                #self.node.dead = False
            char = 'Bones'
            factory = self.spaz.getFactory()
            media = factory._getMedia(char)
            self.spaz.node.colorTexture=media['colorTexture']
            self.spaz.node.colorMaskTexture=media['colorMaskTexture']
            self.spaz.node.headModel=media['headModel']
            self.spaz.node.torsoModel=media['torsoModel']
            self.spaz.node.pelvisModel=media['pelvisModel']
            self.spaz.node.upperArmModel=media['upperArmModel']
            self.spaz.node.foreArmModel=media['foreArmModel']
            self.spaz.node.handModel=media['handModel']
            self.spaz.node.upperLegModel=media['upperLegModel']
            self.spaz.node.lowerLegModel=media['lowerLegModel']
            self.spaz.node.toesModel=media['toesModel']
            self.spaz.node.style=factory._getStyle(char)
        
        elif deff == 'show':doRing(self,deff)
        elif deff == 'xplode':doRing(self,deff)
        elif deff == 'fly':
            if self.spaz.shattered: pass
            def update():
                pos = self.spaz.node.position
                self.spaz.node.handleMessage("impulse",pos[0],pos[1]+0.5,pos[2],0,5,0,3,10,0,0, 0,5,0)
            delay = 0
            for i in range(40):
                bs.gameTimer(delay,bs.Call(update))
                delay += 50
        elif deff == 'skull':
            pos = self.spaz.node.position
            bsUtils.PopupText(bs.getSpecialChar('skull'),color=(1,1,1),scale=5,position=(pos[0],pos[1]-2,pos[2])).autoRetain()
            bs.emitBGDynamics(position=self.spaz.node.position,velocity=self.spaz.node.velocity,count=int(4.0+random.random()*30),emitType='tendrils');
            #bs.emitBGDynamics(position=self.node.position,velocity=(0,10,0),count=100,spread=0.3,scale=3,chunkType='sweat');
        else:
            delay = 0
            for i in range(5):
                bs.gameTimer(delay,bs.Call(doRing,self,deff))
                delay += 300

PlayerSpazDeathMessage.__init__ = newPlayerSpazDeathMessageInit

oldInit = PlayerSpaz.__init__
def newInit(self, color=(1, 1, 1), highlight=(0.5, 0.5, 0.5),  character="Spaz", player=None, powerupsExpire=True):
    oldInit(self, color=color, highlight=highlight, character=character, player=player, powerupsExpire=powerupsExpire)

    eff = bs.getConfig()["effectsMod"]["effect"]

    self.lastPos = self.node.position
    def doCirle():
        if self.isAlive():
            p = self.node.position
            p2 = self.lastPos
            diff = (bs.Vector(p[0]-p2[0],0.0,p[2]-p2[2]))
            dist = (diff.length())
            if dist > 0.2:
                c = bs.getConfig()["effectsMod"]["color"]
                r = bs.newNode('locator',attrs={'shape':'circle','position':p,'color':self.node.color if c else (5,5,5),'opacity':1,'drawBeauty':False,'additive':False,'size':[0.2]})
                bsUtils.animateArray(r,'size',1,{0:[0.2],2500:[0.2],3000:[0]})
                bs.gameTimer(3000,r.delete)
                self.lastPos = self.node.position

    def doFire():
        if self.isAlive():
            bs.emitBGDynamics(position=self.node.position,velocity=(0,10,0),count=100,spread=0.3,scale=3,chunkType='sweat');

    def getPos():
        return self.node.position

    def doEffects():
        if eff == 'path': bs.gameTimer(200,bs.Call(doCirle),repeat=True)	
        elif eff == 'fire': self._color = bs.Timer(100,bs.WeakCall(doFire),repeat=True)

    bs.gameTimer(200,doEffects)

    seff = bs.getConfig()["effectsMod"]["spawnEffect"]
    if seff == "none": pass
    elif seff == 'show':doRing(self,seff)
    elif seff == 'xplode':doRing(self,seff)
    else:
        delay = 0
        for i in range(5):
            bs.gameTimer(delay,bs.Call(doRing,self,seff))
            delay += 300
PlayerSpaz.__init__ = newInit
