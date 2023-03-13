from ursina import *

app = Ursina()

def update():
    pass

def input(key):
    if key == 'q':
        quit()

app.run()