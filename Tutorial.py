from ursina import *
import assets.APIs.player_movement_api as pma
from ursina.prefabs.platformer_controller_2d import PlatformerController2d
import json


with open("data.json", 'r') as f:
    data=json.load(f)

with open("Async tasks.py", "r") as f:
    exec(f.read())


TutorialCompleted=data['TutorialCompleted']
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

if TutorialCompleted:
    app=Ursina()

    Text("Tutorial completed already! To play again chage data to false.",x=-.4)
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


window.vsync=vsyncEnabled
window.fullscreen=Fullscreen
window.title="Echoes in the Dark"
app=Ursina()

app.sfxManagerList[0].setVolume(volume)
player_controller = PlatformerController2d(walk_speed=0,scale_y=.5,scale_x=.25, jump_height=2, z=-1,x=3,model="cube", collider='box', visible=False)

PlayerAnimation=Animation('assets/textures/bat_gif.gif',fps=24,parent=scene,scale=.5,z=0)
camera.position=player_controller.position + (0,7,0)
PlayerAnimation2=Animation('assets/textures/bat_gif2.gif',fps=24,parent=scene,visible=False,scale=.5,z=0)
camera.add_script(SmoothFollow(target=player_controller, offset=[0,1,-30], speed=4))
camera.orthographic = True
camera.fov = 10


with open("GenerateBackground.py", "r") as f:
    exec(f.read())


sky=Entity(model='quad',texture='assets/textures/sky.jpg',z=100,scale=1000,texture_scale=(35,35))
ground = Entity(model='quad', color=color.dark_gray,scale=(1000, 10, 20), collider='box', y=-6, z=player_controller.z+.1)

InSettings=False

def update():
    if player_controller.y<-1.0:
        player_controller.y=-1
    PlayerAnimation.position=player_controller.position+(0,0.2,0)
    PlayerAnimation2.position=player_controller.position+(0,0.2,0)
    #print(InversedMode)
    if InversedMode and not InSettings:
        player_controller.walk_speed=2
    elif not InversedMode and not InSettings:
        player_controller.walk_speed=4

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
        
app.taskMgr.add(LoadAudio(path="assets/audio/main music.ogg",name="Music",autoplay=True,loop=True))
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

    def update(self):
        print(self.collider)
        print(self.ID)
        if player_controller.intersects(self) and self.collider!=None:
            player_controller.x=self.x
        self.position += self.direction * self.speed * time.dt
        if self.position.x > self.toX:
            self.direction = Vec3(-1, 0, 0)
        elif self.position.x < self.fromX:
            self.direction = Vec3(1, 0, 0)
        if self.ID=='Normal':
            self.collider='box'
        else:
            self.collider=None
    def input(self, key):
        if key=='w':
            if self.ID=='Normal':
                self.ID='Inversed'
            else:
                self.ID='Normal'

        
class TutorialBlock(Entity):
    def __init__(self,action, **kwargs):
        super().__init__(self, **kwargs)
        self.action=action
        self.action1Done=False
        self.action2Done=False
    def update(self):
        dist=distance(PlayerAnimation,self)
        if player_controller.y==.25 and dist<.4 and self.action==1:
            destroy(TutorialText,delay=1)
            destroy(self,delay=1)
            if not self.action1Done:
                self.action1Done=True
                invoke(TutorialScript4,delay=1)
        elif dist<.4 and self.action==2:
            self.color=color.rgb(255,0,255)
            if InversedMode:
                destroy(self,delay=2)
                destroy(TutorialText,delay=2)
                if not self.action2Done:
                    self.action2Done=True
                    invoke(TutorialScript12,delay=2)
        if self.action==2 and InversedMode:
            self.color=color.rgb(255,0,255)
            self.collider=None
        elif self.action==2 and not InversedMode:
            self.color=color.black
            self.collider='box'

#MovingPlatformOne=MovingPlatform(ID='Normal',color=color.black33,y=1.5,fromX=6,toX=10)
#Lever1=Interactable(x=10,functionCallBackOn=test,functionCallBackOff=test2,y=-1)
invisWall=Entity(model='cube',color=color.clear,x=-4,scale_y=500,z=player_controller.z-.1,scale_z=20,collider='box')
invisWall1=Entity(model='cube',color=color.clear,x=10,scale_y=500,z=player_controller.z-.1,scale_z=20,collider='box')

TutorialTimer=0
TutorialAction1=False
TutorialAction2=False
TutorialAction3=False

def TutorialTimerUpdate():
    global TutorialTimer,TutorialAction1,TutorialAction2,TutorialText
    if TutorialAction1:
        TutorialTimer+=time.dt
        if TutorialTimer>=4:
            TutorialAction1=False
            destroy(TutorialText)
            TutorialTimer=0
            TutorialScript2()

def TutorialInputs(key):
    global TutorialAction2,TutorialText,TutorialAction3
    if TutorialAction2:
        if key=='space':
            TutorialAction2=False
            invoke(TutorialScript3,delay=1)
            destroy(TutorialText)
            print_on_screen("Nice!",duration=1)
    if TutorialAction3:
        if key=='w':
            destroy(TutorialText)
            TutorialAction3=False
            chance=random.randint(0,20)
            if chance==20:
                Audio('assets/audio/eggyaudio.ogg',autoplay=True,loop=False,auto_destroy=True,volume=2)
                Audio('assets/audio/eggyaudio2.ogg',autoplay=True,loop=False,auto_destroy=True)
                Entity(parent=camera.ui,model='quad',texture='assets/textures/happyboi.jpg',scale=2)
                Music.stop()
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
    puzzleBlockOne=TutorialBlock(action=1,model='quad',color=color.black,z=player_controller.z,y=.1,scale=.3,x=5,collider='box')

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
    TutorialText=Text("You can tell if you can't jump on it by its colour.",scale=1.2,y=.3,x=-.13)
    destroy(TutorialText, delay=3); invoke(TutorialScript11,delay=3)
    PopSound.play()

def TutorialScript11():
    global TutorialText
    if InversedMode:
        TutorialText=Text("For example that block over there, try jump on it.",scale=1.2,y=.3,x=-.13)
    else:
        TutorialText=Text("Go into shadow mode and try jump on that block.",scale=1.2,y=.3,x=-.14)
    puzzleblock=TutorialBlock(ID='Normal',action=2,model='quad',z=player_controller.z,y=.1,scale=.3,x=5,collider='box')
    PopSound.play()

def TutorialScript12():
    global TutorialText
    TutorialText=Text("See! Very cool, right?",scale=1.2,y=.3,x=-.15)
    destroy(TutorialText,delay=2)
    invoke(TutorialScript13,delay=2)
    PopSound.play()

def TutorialScript13():
    global TutorialText
    TutorialText=Text("Moving platforms, also, can't be walked on in shadow mode.",scale=1.2,y=.3,x=-.25)
    PopSound.play()
    destroy(TutorialText,delay=4); invoke(TutorialScript14,delay=4)

def TutorialScript14():
    global TutorialText
    TutorialText=Text("Ok, lets move onto the main game!",scale=1.2,y=.3,x=-.12)
    PopSound.play()
    invoke(FinishedTutorial,delay=3)

def FinishedTutorial():
    Level1Completed = True
    data['Level1Completed'] = Level1Completed
    with open("data.json", "w") as f:
        json.dump(data, f,indent=4)
        Audio('assets/audio/levelwin',autoplay=True,loop=False)
    camera.overlay.color = color.black
    egg = Sprite(name='cheese', parent=camera.ui, texture='assets/textures/leveldone.png', world_z=camera.overlay.z-1, scale=.1, color=color.white)
    invoke(nextpart,delay=3.2)
def nextpart():
    import subprocess
    import sys
    import os

    current_dir = os.path.abspath(os.path.dirname(sys.argv[0]))

    file_path = os.path.join(current_dir, "level2.py")

    subprocess.Popen(["python", file_path])
    sys.exit()

TutorialScript1()

app.run()