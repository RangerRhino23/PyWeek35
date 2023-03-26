from ursina import *
import assets.APIs.player_movement_api as pma
from ursina.prefabs.platformer_controller_2d import PlatformerController2d
import json

with open("data.json", 'r') as f:
    data=json.load(f)

Level1Complete=data['Level1Completed']

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

app.sfxManagerList[0].setVolume(volume/100)
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
ground = Entity(model='cube', color=color.dark_gray,origin_y=.1 ,scale=(1000, 10, 1), collider='box', y=-5)

def update():
    PlayerAnimation.z=-5
    PlayerAnimation.x=player_controller.x
    PlayerAnimation.y=player_controller.y
    PlayerAnimation2.z=-5
    PlayerAnimation2.x=player_controller.x
    PlayerAnimation2.y=player_controller.y
    pma.player_movement(player_controller, 3)

def input(key):
    if key=='a' or held_keys=='a' and not held_keys['d']:
        PlayerAnimation2.visible=True
        PlayerAnimation.visible=False
    if key=='d' or held_keys['d'] and not held_keys['a']:
        PlayerAnimation2.visible=False
        PlayerAnimation.visible=True

app.run()