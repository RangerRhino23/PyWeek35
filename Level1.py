from ursina import *
import random as ra
import numpy as np
import assets.APIs.player_movement_api as pma
from ursina.prefabs.platformer_controller_2d import PlatformerController2d
import os


app=Ursina()

CustomColor = rgb
rock_color = CustomColor(55, 55, 55)


player_controller = PlatformerController2d(scale_y=2, jump_height=2, x=3,model=None, y=20)

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
    pma.player_movement(player_controller, .8)

def input(key):
    if key=='a' or held_keys=='a' and not held_keys['d']:
        PlayerAnimation2.visible=True
        PlayerAnimation.visible=False
    if key=='d' or held_keys['d'] and not held_keys['a']:
        PlayerAnimation2.visible=False
        PlayerAnimation.visible=True

app.run()