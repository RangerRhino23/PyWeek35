from ursina import *
import random as ra

app=Ursina()

for x in range(0,100, 20):
    randomBuilding=ra.randint(1,2)
    if randomBuilding==1:
        bg1=Entity(model='quad',texture='assets/textures/building1', x=x)
    elif randomBuilding==2:
        bg2=Entity(model='quad',texture='assets/textures/building2', x=x)

app.run()