from ursina import *

#Version: 2.0

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


def entity_movement(entity, speed, keys):
    if keys[0] == True:
        if held_keys['w']:
            entity.y += speed * time.dt
    if keys[1] == True:
        if held_keys['a']:
            entity.x -= speed * time.dt
    if keys[2] == True:
        if held_keys['s']:
            entity.y -= speed * time.dt
    if keys[3] == True:
        if held_keys['d']:
            entity.x += speed * time.dt