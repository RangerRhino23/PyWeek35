from ursina import *
import random as ra
from ursina.prefabs.platformer_controller_2d import PlatformerController2d

app=Ursina()
player_controller = PlatformerController2d(scale_y=2, jump_height=4, x=3,model=None, y=20)
camera.add_script(SmoothFollow(target=player_controller, offset=[0,1,-30], speed=4))
PlayerAnimation=Animation('assets/textures/bat_gif.gif',parent=scene,scale=2,z=-5)
camera.orthographic = True
camera.fov = 10

def update():
    PlayerAnimation.z=-5
    PlayerAnimation.x=player_controller.x
    PlayerAnimation.y=player_controller.y

app.run()