from ursina import *

app = Ursina()

def update():
    pass

def input(key):
    if key == 'q':
        application.quit()

app.run()