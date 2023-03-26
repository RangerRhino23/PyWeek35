from ursina import *

#Version: 1.2

###SETUP###
#REQUIREMENTS: base_speed = 1 and player = Entity()

#Import api: import assets.APIs.player_movement_api as pm

#In update function (def update():): pm.player_movement(player, base_speed)

def player_movement(player, base_speed):
    if held_keys['w']:
        player.y += base_speed * time.dt
    if held_keys['a']:
        player.x -= base_speed * time.dt
    if held_keys['s']:
        player.y -= base_speed * time.dt
    if held_keys['d']:
        player.x += base_speed * time.dt