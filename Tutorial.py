from ursina import *
import assets.APIs.player_movement_api as pma
from ursina.prefabs.platformer_controller_2d import PlatformerController2d
import json


with open("data.json", 'r') as f:
    data=json.load(f)

with open("Async tasks.py", "r") as f:
    exec(f.read())

with open("SettingsFunctions.py", "r") as f:
    exec(f.read())


Level1Complete=data['Level1Completed']
InversedMode=False

def Inverse():
    inverse_paths = {}
    for i in range(1, 10):
        inverse_paths[i] = 'assets/textures/buildingsInverse/building{}.png'.format(i)

    if not hasattr(Inverse, 'state'):
        Inverse.state = 'normal'
    
    if Inverse.state == 'normal':
        for e in scene.entities:
            if isinstance(e, Entity) and e.texture is not None:
                if isinstance(e.texture, Texture) and e.texture.path is not None:
                    texture_path = e.texture.path
                elif isinstance(e.texture, str):
                    texture_path = e.texture
                else:
                    texture_path = None
                
                if texture_path is not None:
                    filename = os.path.basename(texture_path)
                    if filename.startswith('building') and filename.endswith('.png'):
                        building_num = filename[8]
                        if building_num.isdigit() and int(building_num) in range(1, 10):
                            inverse_path = inverse_paths[int(building_num)]
                            e.texture = inverse_path
        
        Inverse.state = 'inverse'
    
    elif Inverse.state == 'inverse':
        for e in scene.entities:
            if isinstance(e, Entity) and e.texture is not None:
                if isinstance(e.texture, Texture) and e.texture.path is not None:
                    texture_path = e.texture.path
                elif isinstance(e.texture, str):
                    texture_path = e.texture
                else:
                    texture_path = None
                
                if texture_path is not None:
                    filename = os.path.basename(texture_path)
                    if filename.startswith('building') and filename.endswith('.png'):
                        building_num = filename[8]
                        if building_num.isdigit() and int(building_num) in range(1, 10):
                            normal_path = 'assets/textures/buildings/building{}.png'.format(building_num)
                            e.texture = normal_path
                Inverse.state = 'normal'
    for e in scene.entities:
        if Inverse.state == 'inverse':
            if hasattr(e, "ID"):
                if e.ID=="Normal":
                    e.color=color.rgb(255,0,255)
                    e.collider=None
                if e.ID=="Inversed":
                    e.color=color.black33
                    e.collider='box'
        else:
            if hasattr(e, "ID"):
                if e.ID=="Normal":
                    e.color=color.black33
                    e.collider='box'
                if e.ID=="Inversed":
                    e.color=color.rgb(255,0,255)
                    e.collider=None

if Level1Complete:
    app=Ursina()

    Text("Level 1 completed already!")
    timer=0

    def update():
        global timer
        timer+=time.dt
        if timer>=5:
            application.quit()
    app.run()

vsyncEnabled=data['vsyncEnabled']
Fullscreen=data['Fullscreen']
MasterVolume=data['MasterVolume']
volume=data['MasterVolume']/100
Level1Completed=data['Level1Completed']


window.vsync=vsyncEnabled
window.fullscreen=Fullscreen
window.title="Echoes in the Dark"
app=Ursina()

app.sfxManagerList[0].setVolume(volume)
player_controller = PlatformerController2d(walk_speed=0,scale_y=.5,scale_x=.25, jump_height=2, z=-1,x=3,model="cube", y=20, collider='box', visible=False)

PlayerAnimation=Animation('assets/textures/bat_gif.gif',fps=24,parent=scene,scale=.5,z=0)
camera.position=player_controller.position + (0,7,0)
PlayerAnimation2=Animation('assets/textures/bat_gif2.gif',fps=24,parent=scene,visible=False,scale=.5,z=0)
camera.add_script(SmoothFollow(target=player_controller, offset=[0,1,-30], speed=4))
camera.orthographic = True
camera.fov = 10


with open("GenerateBackground.py", "r") as f:
    exec(f.read())


sky=Entity(model='quad',texture='assets/textures/sky.jpg',z=100,scale=1000,texture_scale=(35,35))
ground = Entity(model='quad', color=color.dark_gray,origin_y=.1 ,scale=(1000, 10, 1), collider='box', y=-5, z=-1)

InSettings=False

def update():
    if player_controller.y<-1.1:
        player_controller.y=-1.05
    PlayerAnimation.position=player_controller.position+(0,0.2,0)
    PlayerAnimation2.position=player_controller.position+(0,0.2,0)
    #print(InversedMode)
    if InversedMode and not InSettings:
        pma.player_movement(player_controller, 1.5)
    elif not InversedMode and not InSettings:
        pma.player_movement(player_controller, 3)

Timer=0
InverseCooldown=False  
def InverseTimer():
    global Timer,InverseCooldown
    if InverseCooldown:
        Timer+=time.dt
        if Timer>=1:
            InverseCooldown=False
            Timer=0

Entity(update=InverseTimer)

InverseUnlocked=False

def input(key):
    global InSettings,InverseCooldown,InversedMode
    if key=='w' and not InverseCooldown and not InSettings and InverseUnlocked:
        Inverse()
        InverseCooldown=True
        if InversedMode:
            InversedMode=False
        else:
            InversedMode=True
    if key=='space' and player_controller.y<=-1:
        player_controller.grounded=True
        player_controller.air_time = 0
        player_controller.jumps_left=1
        player_controller.jump()
    if key=='a' or held_keys=='a' and not held_keys['d']:
        PlayerAnimation2.visible=True
        PlayerAnimation.visible=False
    if key=='d' or held_keys['d'] and not held_keys['a']:
        PlayerAnimation2.visible=False
        PlayerAnimation.visible=True
    if key=='escape' and InSettings==False:
        InSettings=True
        with open("Settings.py", "r") as f:
            exec(f.read())
        
app.taskMgr.add(LoadAudio(path="assets/audio/ambient.ogg",name="Ambience1",autoplay=True,loop=True))
app.taskMgr.add(LoadAudio(path="assets/audio/lever.ogg",name="LeverClick",autoplay=False,loop=False))
PopSound=Audio('assets/audio/pop.ogg',autoplay=False,loop=False)
##############
# BUILD AREA #
##############

class MovingPlatform(Entity):
    def __init__(self,ID, fromX, toX,y=0,x=0, **kwargs):
        super().__init__(self,model='quad', parent=scene,z=player_controller.z,x=x,y=y, **kwargs)
        self.fromX=fromX
        self.toX=toX
        self.ID=ID
        self.collider='box'
        self.scale_x=.8
        self.scale_y=.2
        self.color=color.black33
        self.direction = Vec3(1, 0, 0)
        self.speed = 2
        self.x=fromX
        self.y=y
        self.hasCollider=True

    def update(self):
        if player_controller.intersects(self) and self.hasCollider:
            player_controller.x=self.x
        self.position += self.direction * self.speed * time.dt
        if self.position.x > self.toX:
            self.direction = Vec3(-1, 0, 0)
        elif self.position.x < self.fromX:
            self.direction = Vec3(1, 0, 0)
        if self.ID=='Normal':
            self.collider='box'
            self.hasCollider=True
        else:
            self.collider=None
            self.hasCollider=False
        
class Interactable(Entity):
    def __init__(self,functionCallBackOn,functionCallBackOff=None, **kwargs):
        super().__init__(self,model='quad',z=player_controller.z+.1,color=color.black, **kwargs)
        self.scale=1
        self.functionCallBackOn = functionCallBackOn
        self.functionCallBackOff = functionCallBackOff
        self.duration=0
        self.TurnedOn=False

    def update(self):
        if self.TurnedOn:
            self.texture='assets/textures/lever_on.png'
        else:
            self.texture='assets/textures/lever_off.png'

    def input(self, key):
        self.dist=distance(self,player_controller)
        if self.dist<.3 and key=='e':
            if self.TurnedOn:
                self.TurnedOn=False
                if self.functionCallBackOff!=None:
                    invoke(self.functionCallBackOff,delay=self.duration)
            else:
                self.TurnedOn=True
                if self.functionCallBackOn!=None:
                    invoke(self.functionCallBackOn,delay=self.duration)
            LeverClick.play()

class TutorialBlock(Entity):
    def __init__(self, **kwargs):
        super().__init__(self, **kwargs)

    def update(self):
        dist=distance(PlayerAnimation,self)
        if player_controller.y==.25 and dist<.4:
            destroy(TutorialText)
            destroy(self)
            TutorialScript4()

def test():
    print("yes")

def test2():
    print("no")

Wall=Entity(model='cube',color=color.gray,z=player_controller.z,x=-10,scale_y=50,collider='box')
#puzzleBlockOne=Entity(ID="Normal",model='quad',color=color.black33,z=player_controller.z,y=.1,scale=.3,x=2,collider='box')
#PuzzleBlockTwo=Entity(ID="Inversed",model='quad',color=color.rgb(255,0,255),z=player_controller.z,x=4,scale=.3,y=1.5)
#PuzzleBlockThreeEntity=Entity(ID="Normal",model='quad',color=color.black33,z=player_controller.z,x=10.5,scale=.3,y=1.5)
#MovingPlatformOne=MovingPlatform(ID='Normal',color=color.black33,y=1.5,fromX=6,toX=10)
#Lever1=Interactable(x=10,functionCallBackOn=test,functionCallBackOff=test2,y=-1)

TutorialTimer=0
TutorialAction1=False
TutorialAction2=False
TutorialAction3=False

def TutorialTimerUpdate():
    global TutorialTimer,TutorialAction1,TutorialAction2,TutorialText
    print(player_controller.position)
    if TutorialAction1:
        TutorialTimer+=time.dt
        if TutorialTimer>=4:
            TutorialAction1=False
            destroy(TutorialText)
            TutorialTimer=0
            TutorialScript2()

def TutorialInputs(key):
    global TutorialAction2,TutorialText
    if TutorialAction2:
        if key=='space':
            TutorialAction2=False
            invoke(TutorialScript3,delay=1)
            destroy(TutorialText)
            print_on_screen("Nice!",duration=1)
    if TutorialAction3:
        if key=='w':
            destroy(TutorialText)
            chance=20
            if chance==random.randint(0,20):
                Audio('assets/audio/eggyaudio.ogg',autoplay=True,loop=False,auto_destroy=True)
                Audio('assets/audio/eggyaudio2.ogg',autoplay=True,loop=False,auto_destroy=True)
                Entity(parent=camera.ui,model='quad',texture='assets/textures/happyboi.jpg',scale=2)
                Ambience1.stop()
                s = Sequence(
                    Wait(5),
                    Func(application.quit))
                s.start()
            else:
                invoke(TutorialScript7)

Entity(update=TutorialTimerUpdate, input=TutorialInputs)

"""
The code would be much cleaner if I knew how to do sequences but I don't so
this shall work for the time being.
"""
def TutorialScript1():
    global TutorialAction1,TutorialText
    TutorialText=Text("Welcome to the game.",scale=1.2,y=.3,x=-.11)
    PopSound.play()
    TutorialAction1=True

def TutorialScript2():
    global TutorialAction2,TutorialText
    TutorialText=Text("To begin try jump with the spacebar.",scale=1.2,y=.3,x=-.14)
    PopSound.play()
    TutorialAction2=True

def TutorialScript3():
    global TutorialText
    PopSound.play()
    TutorialText=Text("Ok, try jump on that block over there.",scale=1.2,y=.3,x=-.14) 
    puzzleBlockOne=TutorialBlock(model='quad',color=color.black,z=player_controller.z,y=.1,scale=.3,x=5,collider='box')

def TutorialScript4():
    global TutorialText
    TutorialText=Text("Nicely Done!",scale=1.2,y=.3,x=-.1)
    PopSound.play()
    invoke(TutorialScript5,delay=1.5)

def TutorialScript5():
    global TutorialText
    destroy(TutorialText)
    TutorialText=Text("There a few abilities that you have in this game.",scale=1.2,y=.3,x=-.14)
    destroy(TutorialText,delay=3)
    PopSound.play()
    invoke(TutorialScript6,delay=3)

def TutorialScript6():
    global TutorialText,TutorialAction3,InverseUnlocked
    PopSound.play()
    TutorialText=Text("Try clicking 'w' on your keyboard.",scale=1.2,y=.3,x=-.12)
    InverseUnlocked=True
    TutorialAction3=True

def TutorialScript7():
    global TutorialText
    TutorialText=Text("This is called 'Shadow mode'",scale=1.2,y=.3,x=-.13)
    PopSound.play()
    destroy(TutorialText,delay=2)
    invoke(TutorialScript8,delay=2)

def TutorialScript8():
    global TutorialText
    TutorialText=Text("In shadow mode you move slower but you can see invisible blocks.",scale=1.2,y=.3,x=-.2)
    destroy(TutorialText,delay=3)
    invoke(TutorialScript9,delay=3)
    PopSound.play()

def TutorialScript9():
    global TutorialText
    TutorialText=Text("And... when in shadow mode you can't jump on invisible blocks.",scale=1.2,y=.3,x=-.15)
    destroy(TutorialText,delay=3)
    invoke(TutorialScript10,delay=3)
    PopSound.play()

def TutorialScript10():
    global TutorialText
    TutorialText=Text("")
    PopSound.play()
def FinishedTutorial():
    pass
TutorialScript1()

app.run()