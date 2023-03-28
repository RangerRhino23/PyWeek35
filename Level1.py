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
                    e.color=color.black66
                    e.collider='box'
        else:
            if hasattr(e, "ID"):
                if e.ID=="Normal":
                    e.color=color.black66
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
player_controller = PlatformerController2d(walk_speed=0,scale_y=2, jump_height=2, x=3,model=None, y=20)

PlayerAnimation=Animation('assets/textures/bat_gif.gif',fps=24,parent=scene,scale=.5,z=-5)
camera.position=player_controller.position + (0,7,0)
PlayerAnimation2=Animation('assets/textures/bat_gif2.gif',fps=24,parent=scene,visible=False,scale=.5,z=-5)
camera.add_script(SmoothFollow(target=PlayerAnimation, offset=[0,1,-30], speed=4))
camera.orthographic = True
camera.fov = 10


with open("GenerateBackground.py", "r") as f:
    exec(f.read())


sky=Entity(model='quad',texture='assets/textures/sky.jpg',z=100,scale=1000,texture_scale=(30,30))
ground = Entity(model='quad', color=color.dark_gray,origin_y=.1 ,scale=(1000, 10, 1), collider='box', y=-5)

InSettings=False
def update():
    PlayerAnimation.z=-5
    PlayerAnimation.x=player_controller.x
    PlayerAnimation.y=player_controller.y
    PlayerAnimation2.z=-5
    PlayerAnimation2.x=player_controller.x
    PlayerAnimation2.y=player_controller.y
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

def input(key):
    global InSettings,InverseCooldown
    if key=='w' and not InverseCooldown:
        Inverse()
        InverseCooldown=True
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

#############
# TEST AREA #
#############

class MovingPlatform(Entity):
    def __init__(self,ID, fromX, toX,y=0,x=0, **kwargs):
        super().__init__(self,model='quad',collider='box', parent=scene,z=player_controller.z,x=x,y=y)
        self.fromX=fromX
        self.toX=toX
        self.ID=ID
        self.scale_x=.8
        self.scale_y=.2
        self.color=color.black66
        self.direction = Vec3(1, 0, 0)
        self.speed = 2
        self.x=fromX
        self.y=y
        self.hasCollider=True

    def update(self):
        print(player_controller.y)
        print(self.y)
        self.dist=distance(self,player_controller)
        if self.dist<.6 and self.hasCollider:
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

puzzleBlockOne=Entity(ID="Normal",model='quad',color=color.black66,z=player_controller.z,scale=.3,x=2,collider='box')
PuzzleBlackTwo=Entity(ID="Inversed",model='quad',color=color.rgb(255,0,255),z=player_controller.z,x=4,scale=.3,y=1)
MovingPlatformOne=MovingPlatform(ID='Normal',color=color.black66,y=1,fromX=6,toX=10)


app.run()