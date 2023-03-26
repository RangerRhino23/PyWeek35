from ursina import *
import random as ra


app=Ursina()

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

app.run()