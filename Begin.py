from ursina import *
import random as ra
import numpy as np
from ursina.prefabs.platformer_controller_2d import PlatformerController2d


app=Ursina()

CustomColor = rgb
rock_color = CustomColor(55, 55, 55)

player_controller = PlatformerController2d(scale_y=2, jump_height=4, x=3,model=None, y=20)
camera.add_script(SmoothFollow(target=player_controller, offset=[0,1,-30], speed=4))
PlayerAnimation=Animation('assets/textures/bat_gif.gif',parent=scene,scale=.5,z=-5)
camera.orthographic = True
camera.fov = 10

for x in range(0,100, 1):
    randomBuilding=ra.randint(1,2)
    if randomBuilding==1:
        Entity(model='quad',texture='assets/textures/building1', x=x, scale=(1,2))
    elif randomBuilding==2:
        Entity(model='quad',texture='assets/textures/building2', x=x, scale=(1,2))

for xM in range(-1,-100,-1):
    randomBuilding=ra.randint(1,2)
    if randomBuilding==1:
        Entity(model='quad',texture='assets/textures/building1', x=xM, scale=(1,2))
    elif randomBuilding==2:
        Entity(model='quad',texture='assets/textures/building2', x=xM, scale=(1,2))

for x in np.arange(0.0, 100.0, ra.uniform(1.0, 3.0)):
    for y in np.arange(1.0, -5.0, ra.uniform(-3.0, -1.0)):
        if y>-1.005:
            y=ra.uniform(-1.005,-3)
        rock = Entity(model='quad', color=rock_color, scale=.1, y=y, x=x, z=ra.uniform(-5.0, -1.0))

sky=Entity(model='quad',texture='assets/textures/sky.jpg',z=100,scale=100)
ground = Entity(model='cube', color=color.white33,origin_y=.1 ,scale=(100, 10, 1), collider='box', y=-5)

def update():
    PlayerAnimation.z=-5
    PlayerAnimation.x=player_controller.x
    PlayerAnimation.y=player_controller.y
app.run()