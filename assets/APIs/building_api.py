from ursina import *


class Building(Entity):
    def __init__(self, position, side_textures):
        super().__init__()
        self.cube_side = Entity(model='quad', texture=side_textures, position=position+(0,-0.5,-0.5), rotation_y=0)
        self.cube_side = Entity(model='quad', texture=side_textures, position=position+(0,-0.5,.5), rotation_y=180)
        self.cube_side = Entity(model='quad', texture=side_textures, position=position+(-0.5,-0.5,0), rotation_y=90)
        self.cube_side = Entity(model='quad', texture=side_textures, position=position+(0.5,-0.5,0), rotation_y=270)