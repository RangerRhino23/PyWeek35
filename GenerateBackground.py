import random as ra
import numpy as np
import os
#Gets all the images from the buildings folder
imageDirectory = 'assets/textures/buildings'
buildingPool = []
for filename in os.listdir(imageDirectory):
    if filename.endswith('.png'):
        buildingPool.append(Texture(os.path.join(imageDirectory, filename)))
print(buildingPool)
CustomColor = rgb
rock_color = CustomColor(55, 55, 55)
prevBuilding=None

#Creates buildings to the right of 0,0
for x in range(0,100, 1):
    randomBuilding = ra.choice(buildingPool)
    while randomBuilding == prevBuilding:
        randomBuilding = ra.choice(buildingPool)
    prevBuilding=randomBuilding
    Entity(model='quad',texture=randomBuilding,x=x,scale=(1,2))

#Creates buildings to the left of 0,0
for xM in range(-1,-100,-1):
    randomBuilding = ra.choice(buildingPool)
    while randomBuilding == prevBuilding:
        randomBuilding = ra.choice(buildingPool)
    prevBuilding=randomBuilding
    Entity(model='quad',texture=randomBuilding,x=xM,scale=(1,2))

for x in np.arange(0.0, 100.0, ra.uniform(1.0, 3.0)):
    for y in np.arange(1.0, -5.0, ra.uniform(-3.0, -1.0)):
        if y>-1.005:
            y=ra.uniform(-1.005,-3)
        rock = Entity(model='quad', color=rock_color, scale=.1, y=y, x=x, z=ra.uniform(-5.0, -1.0))

for x in np.arange(0.0, -100.0, ra.uniform(-1.0, -3.0)):
    for y in np.arange(1.0, -5.0, ra.uniform(-3.0, -1.0)):
        if y>-1.005:
            y=ra.uniform(-1.005,-3)
        rock = Entity(model='quad', color=rock_color, scale=.1, y=y, x=x, z=ra.uniform(-5.0, -1.0))
