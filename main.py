from ursina import *
import assets.APIs.player_movement_api as pma

app = Ursina()
window.fullscreen = True



def update():
    pma.player_movement(a,5)

def input(key):
    if key == 'q' or key == 'esc':
        application.quit()

a = Animation('assets/textures/bat_gif.gif', scale=7)

app.run()