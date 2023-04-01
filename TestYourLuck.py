from ursina import *
import random as ra
from ursina.prefabs.platformer_controller_2d import PlatformerController2d

class MovingPlatform(Entity):
    def init(self,ID, fromY, toY,x=0,y=0, kwargs):
        super().init(self,model='quad', parent=scene,x=x,y=y, **kwargs)
        self.fromY=fromY
        self.toY=toY
        self.ID=ID
        self.collider='box'
        self.scale_x=.8
        self.scale_y=.2
        self.color=color.black33
        self.direction = Vec3(0, 1, 0)
        self.speed = 2
        self.x=x
        self.y=fromY # modified to set the starting position in the y-axis
        self.hasCollider=True

    def update(self):
        if player_controller.intersects(self) and self.hasCollider:
            player_controller.y=self.y
        self.position += self.direction * self.speed * time.dt
        if self.position.y > self.toY:
            self.direction = Vec3(0, -1, 0)
        elif self.position.y < self.fromY:
            self.direction = Vec3(0, 1, 0)
        if self.ID=='Normal':
            self.collider='box'
            self.hasCollider=True
        else:
            self.collider=None
            self.hasCollider=False
app=Ursina()

def Funct():
    pass

Interactable(functionCallBackOn=Funct)


app.run()