from ursina import *
import random as ra
from ursina.prefabs.platformer_controller_2d import PlatformerController2d

class Interactable(Entity):
    def __init__(self,functionCallBackOn,functionCallBackOff=None, **kwargs):
        super().__init__(self,model='quad',z=0+.1, **kwargs)
        self.scale=1
        self.functionCallBackOn = functionCallBackOn
        self.functionCallBackOff = functionCallBackOff
        self.duration=0
        self.TurnedOn=False

    def update(self):
        if self.TurnedOn:
            self.texture='assets/textures/lever_on.png'
        else:
            self.texture='assets/textures/lever_off.png'

    def input(self, key):
        if key=='e':
            if self.TurnedOn:
                self.TurnedOn=False
                if self.functionCallBackOff!=None:
                    invoke(self.functionCallBackOff,delay=self.duration)
            else:
                self.TurnedOn=True
                if self.functionCallBackOn!=None:
                    invoke(self.functionCallBackOn,delay=self.duration)
            Audio("assets/audio/lever.ogg",auto_destroy=True,autoplay=True)

app=Ursina()

def Funct():
    pass

Interactable(functionCallBackOn=Funct)


app.run()