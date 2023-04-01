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


vsyncEnabled=data['vsyncEnabled']
Fullscreen=data['Fullscreen']
MasterVolume=data['MasterVolume']
volume=data['MasterVolume']/100
Level5Completed=data['Level5Completed']


window.vsync=vsyncEnabled
window.fullscreen=Fullscreen
window.title="Echoes in the Dark"


app=Ursina()
time.sleep(1)
camera.overlay.color = color.black
logo = Sprite(name='ursina_splash', parent=camera.ui, texture='assets/textures/intro5.png', world_z=camera.overlay.z-1, scale=.1, color=color.clear)
logo.animate_color(color.white, duration=2, delay=1, curve=curve.out_quint_boomerang)
camera.overlay.animate_color(color.clear, duration=1, delay=4)
destroy(logo, delay=5)

def splash_input(key):
    destroy(logo)
    camera.overlay.animate_color(color.clear, duration=.25)

logo.input = splash_input

app.sfxManagerList[0].setVolume(volume)
player_controller = PlatformerController2d(parent=scene,walk_speed=2,scale_y=.5,scale_x=.25, jump_height=2, z=-1,x=3,model="cube", visible=False)

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

def input(key):
    global InSettings,InverseCooldown,InversedMode
    if key=='w' and not InverseCooldown and not InSettings:
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
    ###TESTING###
    if key == 'g':
        player_controller.position = movingPlatformOne.position

app.taskMgr.add(LoadAudio(path="assets/audio/lever.ogg",name="LeverClick",autoplay=False,loop=False))
app.taskMgr.add(LoadAudio(path="assets/audio/main music.ogg",name="Music",autoplay=True,loop=True))

##############
# BUILD AREA #
##############

class MovingPlatform(Entity):
    def __init__(self,ID, fromX, toX,y=0,x=0, **kwargs):
        super().__init__(self,model='quad', parent=scene,z=player_controller.z,x=x,y=y, **kwargs)
        self.fromX=fromX
        self.toX=toX
        self.id=ID
        self.collider='box'
        self.scale_x=.8
        self.scale_y=.2
        self.color=color.black33
        self.direction = Vec3(1, 0, 0)
        self.speed = 2
        self.x=fromX
        self.y=y
        self.Timer=0

    def update(self):
        if player_controller.intersects(self) and self.collider!=None:
            player_controller.x=self.x
        self.position += self.direction * self.speed * time.dt
        if self.position.x > self.toX:
            self.direction = Vec3(-1, 0, 0)
        elif self.position.x < self.fromX:
            self.direction = Vec3(1, 0, 0)
        if self.id=='Normal':
            self.collider='box'
            self.color=color.black33
        else:
            self.collider=None
            self.color=color.rgb(255,0,255)
        if self.Timer>=.00001:
            self.Timer+=time.dt
            if self.Timer>=1:
                self.Timer=0

    def input(self, key):
        if key=='w' and self.Timer==0:
            self.Timer=.00001
            if self.id=='Normal':
                self.id='Inversed'
            elif self.id=='Inversed':
                self.id='Normal'

class MovingPlatform_Vertical(Entity):
    def __init__(self,ID, fromY, toY,x=0,y=0, **kwargs):
        super().__init__(self,model='quad', parent=scene,z=player_controller.z,x=x,y=y, **kwargs)
        self.fromY=fromY
        self.toY=toY
        self.id=ID
        self.collider='box'
        self.scale_x=.8
        self.scale_y=.2
        self.color=color.black33
        self.direction = Vec3(0, 1, 0) # modified to move up and down
        self.speed = 2
        self.Timer=0
        self.x=x
        self.y=fromY # modified to set the starting position in the y-axis

    def update(self):
        if player_controller.intersects(self) and self.collider!=None:
            player_controller.y=self.y+.1 # modified to update player's y-axis position
        self.position += self.direction * self.speed * time.dt
        if self.position.y > self.toY: # modified to check against the top boundary
            self.direction = Vec3(0, -1, 0)
        elif self.position.y < self.fromY: # modified to check against the bottom boundary
            self.direction = Vec3(0, 1, 0)
        if self.id=='Normal':
            self.collider='box'
            self.color=color.black33
        else:
            self.collider=None
            self.color=color.rgb(255,0,255)
        if self.Timer>=.00001:
            self.Timer+=time.dt
            if self.Timer>=1:
                self.Timer=0

    def input(self, key):
        if key=='w' and self.Timer==0:
            self.Timer=.00001
            if self.id=='Normal':
                self.id='Inversed'
            elif self.id=='Inversed':
                self.id='Normal'

class Interactable(Entity):
    def __init__(self,functionCallBackOn,functionCallBackOff=None, **kwargs):
        super().__init__(self,model='quad', **kwargs)
        self.scale=(.2,.4)
        self.functionCallBackOn = functionCallBackOn
        self.functionCallBackOff = functionCallBackOff
        self.duration=0
        self.z=player_controller.z+.1
        self.TurnedOn=False

    def update(self):
        if self.TurnedOn:
            self.texture='assets/textures/lever_on.png'
        else:
            self.texture='assets/textures/lever_off.png'

    def input(self, key):
        self.dist=distance(self,player_controller)
        if self.dist<.4 and key=='e':
            if self.TurnedOn:
                self.TurnedOn=False
                if self.functionCallBackOff!=None:
                    invoke(self.functionCallBackOff,delay=self.duration)
            else:
                self.TurnedOn=True
                if self.functionCallBackOn!=None:
                    invoke(self.functionCallBackOn,delay=self.duration)
            LeverClick.play()

defaultPlayerPosition=Vec3(player_controller.position)
class LaserBeam(Entity):
    def __init__(self,ID,x=0,y=0,cooldown_speed=1.1, **kwargs):
        super().__init__(self, **kwargs)
        self.model='quad'
        self.scale=(0.125,y)
        self.x=x
        self.y=y
        self.z=player_controller.z
        self.ID=ID
        self.color=color.red
        self.visible = True
        self.name = 'LaserBeam'
        self.cooldown_speed=cooldown_speed
        self.cooldown=0
        self.biggusCollidus=Entity(model='quad',color=color.clear,position=self.position,scale_y=self.scale_y+.08,scale_x=self.scale_x+.08,z=player_controller.z)

    def update(self):
        self.cooldown += time.dt
        if self.cooldown >= self.cooldown_speed:
            self.cooldown = 0
            if self.visible:
                self.visible = False
            else:
                self.visible = True
        if player_controller.intersects(self.biggusCollidus):
            player_controller.position=Vec3(defaultPlayerPosition)
        if self.visible:
            self.biggusCollidus.collider='box'
        else:
            self.biggusCollidus.collider=None
        if self.ID == 'Normal':
            self.color = color.red
        elif self.ID == 'Inversed':
            self.color = rgb(255,0,255)

class Door(Entity):
    def __init__(self,locked, **kwargs):
        super().__init__(self, **kwargs)
        self.locked=locked
        self.model='quad'
        self.collider=None
        self.scale_y=.8
        self.z=player_controller.z+.1
        self.scale_x=.4
        self.texture='assets/textures/doorClosed.png'
        self.inviscollider=Entity(model='quad',color=color.clear,scale_y=4,scale_z=2,scale_x=.4)
        self.inviscollider.position=self.position
        self.y-=.1


    def update(self):
        dist=distance(self, player_controller)
        if self.locked:
            self.inviscollider.collider='box'
            self.texture='assets/textures/doorClosed.png'
        else:
            self.inviscollider.collider=None
            self.texture='assets/textures/doorOpened.png'
            if dist<.5:
                FinishedLevel5()
leversPulled=0
def DoorUnlock():
    global leversPulled
    leversPulled+=1
    if leversPulled==3:
        DoorForWall.locked=False

def DoorLock():
    global leversPulled
    leversPulled-=1
    if leversPulled<3:
        DoorForWall.locked=True

invisWall=Entity(model='cube',color=color.clear,x=-50,scale_y=500,z=player_controller.z-.1,scale_z=20,collider='box')
invisWall1=Entity(model='cube',color=color.clear,y=-8,x=20,scale_y=20,z=player_controller.z-.1,scale_z=20,collider='box')
invisWall1=Entity(model='cube',color=color.clear,y=2,x=27,scale_y=20,z=player_controller.z-.1,scale_z=20,collider='box')
DoorForWall=Door(locked=True,y=-.5,x=-2)
blockOne=Entity(ID="Inversed",model='quad',color=rgb(255,0,255),z=player_controller.z,x=5,scale=.3,y=0,collider='box')
blockTwo=Entity(ID="Normal",model='quad',color=color.black33,z=player_controller.z,x=6,scale=.3,y=1,collider='box')
blockThree=Entity(ID="Inversed",model='quad',color=rgb(255,0,255),z=player_controller.z,x=7,scale=.3,y=2,collider='box')
laserBeamOne=LaserBeam(ID='Normal',x=7.5,y=4,cooldown_speed=1)
blockFour=Entity(ID="Normal",model='quad',color=color.black33,z=player_controller.z,x=8,scale=.3,y=2,collider='box')
movingPlatformOne=MovingPlatform(ID='Inversed',color=rgb(255,0,255),y=4,fromX=9,toX=12)
blockFive=Entity(ID="Normal",model='quad',color=color.black33,z=player_controller.z,x=13,scale=.3,y=4,collider='box')
movingPlatformTwo=MovingPlatform_Vertical(ID='Inversed',color=rgb(255,0,255),x=14,fromY=4,toY=14)
blockSix=Entity(ID="Normal",model='quad',color=color.black33,z=player_controller.z,x=13,scale=.3,y=6,collider='box')
blockSeven=Entity(ID="Normal",model='quad',color=color.black33,z=player_controller.z,x=13,scale=.3,y=12,collider='box')
blockEight=Entity(ID="Normal",model='quad',color=color.black33,z=player_controller.z,x=15,scale=.3,y=10,collider='box')


#laserBeamOne=LaserBeam(ID="Normal",x=4,y=0)
#MovingPlatformOne=MovingPlatform_Vertical(ID='Normal',color=color.black66,x=4,fromY=-1,toY=4)
#blockOne=Entity(ID="Inversed",model='quad',color=color.black33,z=player_controller.z,x=5,scale=.3,y=5,collider='box')
#ground2=Entity(model='quad',color=color.dark_gray,scale_y=.5,z=player_controller.z,scale_x=5,x=18,y=4,collider='box')
#LeverForDoor=Interactable(functionCallBackOn=DoorUnlock,functionCallBackOff=DoorLock,x=20,y=4.5)

def FinishedLevel5():
    Level5Completed = True
    data['Level5Completed'] = Level5Completed
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

    file_path = os.path.join(current_dir, "Level6.py")

    subprocess.Popen(["python", file_path])
    sys.exit()

app.run()