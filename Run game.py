from ursina import *
import json
with open("data.json", 'r') as f:
    data=json.load(f)
def StartTutorial():
    import subprocess
    import sys
    import os

    current_dir = os.path.abspath(os.path.dirname(sys.argv[0]))

    file_path = os.path.join(current_dir, "Tutorial.py")

    subprocess.Popen(["python", file_path])
    sys.exit()

def StartProlouge():
    import subprocess
    import sys
    import os

    current_dir = os.path.abspath(os.path.dirname(sys.argv[0]))

    file_path = os.path.join(current_dir, "Prolouge.py")

    subprocess.Popen(["python", file_path])
    sys.exit()

def StartLevel2():
    import subprocess
    import sys
    import os

    current_dir = os.path.abspath(os.path.dirname(sys.argv[0]))

    file_path = os.path.join(current_dir, "Level2.py")

    subprocess.Popen(["python", file_path])
    sys.exit()

def StartLevel3():
    import subprocess
    import sys
    import os

    current_dir = os.path.abspath(os.path.dirname(sys.argv[0]))

    file_path = os.path.join(current_dir, "Level3.py")

    subprocess.Popen(["python", file_path])
    sys.exit()

def StartLevel4():
    import subprocess
    import sys
    import os

    current_dir = os.path.abspath(os.path.dirname(sys.argv[0]))

    file_path = os.path.join(current_dir, "Level4.py")

    subprocess.Popen(["python", file_path])
    sys.exit()

def StartEnd():
    import subprocess
    import sys
    import os

    current_dir = os.path.abspath(os.path.dirname(sys.argv[0]))

    file_path = os.path.join(current_dir, "FinalLevel.py")

    subprocess.Popen(["python", file_path])
    sys.exit()


async def LoadAudio(path, name=None,autoplay=False,loop=False): #Smoothly loads audio files
    global audioname
    audioname = loader.loadSfx(path)
    
    audioname=Audio(audioname,autoplay=autoplay,loop=loop)
    globals()[name] = audioname

def ChangeVsync():
    global vsyncEnabled
    if vsyncEnabled:
        vsyncEnabled=False
        VsyncSetting.text=f'Vsync: off'
        print(vsyncEnabled)
        data["vsyncEnabled"] = False
        info=Text(text='Restart to apply changes',size=.05,font="assets/misc/HighwayItalic-yad3.otf",y=-.3,x=-.25)
        destroy(info,delay=3)
        with open("data.json", "w") as f:
            json.dump(data, f,indent=4)
    else:
        vsyncEnabled=True
        VsyncSetting.text=f'Vsync: on'
        data["vsyncEnabled"] = True
        info=Text(text='Restart to apply changes',size=.05,font="assets/misc/HighwayItalic-yad3.otf",y=-.3,x=-.25)
        destroy(info,delay=3)
        with open("data.json", "w") as f:
            json.dump(data, f,indent=4)

def set_volume():
    global volume_slider,volume
    volume = volume_slider.value/100
    app.sfxManagerList[0].setVolume(volume)
    data['MasterVolume'] = round(volume*100)
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

def ChangeScreen():
    global Fullscreen
    if Fullscreen:
        window.fullscreen=False
        Fullscreen=False
        FullscreenSetting.text=f'Fullscreen: off'
        data['Fullscreen'] = False
        with open("data.json", "w") as f:
            json.dump(data, f, indent=4)
    else:
        window.fullscreen=True
        Fullscreen=True
        FullscreenSetting.text=f'Fullscreen: on'
        data['Fullscreen'] = True
        with open("data.json", "w") as f:
            json.dump(data, f, indent=4)

def SettingsMenu():
    global VsyncSetting,volume_slider,volume,FullscreenSetting, MainMenuSelector
    MainMenuStart.disabled=True; MainMenuStart.visible=False; MainMenuSelector.disabled=True; MainMenuSelector.visible=False
    SettingsMusic.play(); AmbientSound1.stop()
    MainMenuSettings.on_click=SettingsMenuReturn; MainMenuSettings.text='Return'; MainMenuSettings.y=-.3
    if vsyncEnabled:
        VsyncSetting=Button(text=f'Vsync: on',scale_x=.2,scale_y=.1,y=.3,x=-.35,color=color.clear,highlight_color=color.clear,on_click=ChangeVsync)
    else:
        VsyncSetting=Button(text=f'Vsync: off',scale_x=.2,scale_y=.1,y=.3,x=-.35,color=color.clear,highlight_color=color.clear,on_click=ChangeVsync)
    MainMenuQuit.visible=False; MainMenuQuit.disabled=True
    volume_slider = Slider(min=0, max=100, default=volume*100, dynamic=True,position=(-.25, .4),text='Master volume:',on_value_changed = set_volume)
    if Fullscreen:
        FullscreenSetting=Button(text=f'Fullscreen: on',scale_x=.2,scale_y=.1,y=.2,x=-.35,color=color.clear,highlight_color=color.clear,on_click=ChangeScreen)
    else:
        FullscreenSetting=Button(text=f'Fullscreen: off',scale_x=.2,scale_y=.1,y=.2,x=-.35,color=color.clear,highlight_color=color.clear,on_click=ChangeScreen)

def LevelSelector():
    global Level1,Level2,Level3,Level4,Level5,Level6
    MainMenuSelector.on_click=LevelSelectorReturn; MainMenuSelector.text="Return"
    MainMenuStart.disabled=True; MainMenuStart.visible=False
    MainMenuSettings.disabled=True; MainMenuSettings.visible=False
    Level1=Button(LV="Yes",text="Load Tutorial.", on_click=StartTutorial,y=.2,x=-.3,color=color.clear,highlight_color=color.clear,scale=(.2,.1,.1))
    Level2=Button(LV="Yes",text="Load prolouge.", on_click=StartProlouge,y=.0,x=-.3,color=color.clear,highlight_color=color.clear,scale=(.2,.1,.1))
    Level3=Button(LV="Yes",text="Load level 2.", on_click=StartLevel2,y=-.2,x=-.3,color=color.clear,highlight_color=color.clear,scale=(.2,.1,.1))
    Level4=Button(LV="Yes",text="Load level 3.", on_click=StartLevel3,y=.2,x=0,color=color.clear,highlight_color=color.clear,scale=(.2,.1,.1))
    Level5=Button(LV="Yes",text="Load level 4.", on_click=StartLevel4,y=0,x=0,color=color.clear,highlight_color=color.clear,scale=(.2,.1,.1))
    Level6=Button(LV="Yes",text="Load finale.", on_click=StartEnd,y=-.2,x=0,color=color.clear,highlight_color=color.clear,scale=(.2,.1,.1))
Finsfhsdjfh=data['Level5Completed']
def update():
    try:
        if Finsfhsdjfh:
            Level6.on_click=StartEnd
        else:
            Level6.on_click=None
        if Level1.hovered:
            MainMenu.color=color.white66
            MainMenu.texture='assets/textures/tutorial_button.png'
        elif Level2.hovered:
            MainMenu.color=color.white66
            MainMenu.texture='assets/textures/levelone_button.png'
        elif Level3.hovered:
            MainMenu.color=color.white66
            MainMenu.texture='assets/textures/leveltwo_button.png'
        elif Level4.hovered:
            MainMenu.color=color.white66
            MainMenu.texture='assets/textures/levelthree_button.png'
        elif Level5.hovered:
            MainMenu.color=color.white66
            MainMenu.texture='assets/textures/levelfour_button.png'
        elif Level6.hovered:
            MainMenu.color=color.white66
            MainMenu.texture='assets/textures/final_button.png'
        else:
            MainMenu.color=color.black66
            MainMenu.texture=None
    except:
        pass

def LevelSelectorReturn():
    MainMenuSelector.on_click=LevelSelector; MainMenuSelector.text="Level Selector"
    MainMenuStart.disabled=False; MainMenuStart.visible=True
    MainMenuSettings.disabled=False; MainMenuSettings.visible=True
    destroy(Level1); destroy(Level2); destroy(Level3); destroy(Level4); destroy(Level5); destroy(Level6)

def SettingsMenuReturn():
    MainMenuSettings.on_click=SettingsMenu; MainMenuSettings.text='Settings'; MainMenuSettings.y=-.1
    MainMenuStart.disabled=False; MainMenuStart.visible=True; MainMenuSelector.disabled=False; MainMenuSelector.visible=True
    SettingsMusic.stop(); AmbientSound1.play()
    destroy(VsyncSetting); destroy(volume_slider); destroy(FullscreenSetting)
    MainMenuQuit.visible=True; MainMenuQuit.disabled=False

def StartGame():
    import subprocess
    import sys
    import os

    current_dir = os.path.abspath(os.path.dirname(sys.argv[0]))

    file_path = os.path.join(current_dir, "Tutorial.py")

    subprocess.Popen(["python", file_path])
    sys.exit()





global vsyncEnabled,Fullscreen
vsyncEnabled=data['vsyncEnabled']
Fullscreen=data['Fullscreen']
MasterVolume=data['MasterVolume']
volume=data['MasterVolume']/100
Level1Completed=data['Level1Completed']


window.vsync=vsyncEnabled
window.fullscreen=Fullscreen
window.title = "Echoes in the Dark"
app = Ursina(borderless=False)

MainMenu=Entity(parent=camera.ui,model='quad',color=color.black66,scale_y=1,scale_x=2)
MainMenuStart=Button(text='Start Game',scale_y=.1,scale_x=.2,color=color.clear,highlight_color=color.clear,x=-.7,on_click=StartGame)
MainMenuSettings=Button(text='Settings',scale_y=.1,scale_x=.2,color=color.clear,hightlight_color=color.clear,x=-.7,y=-.12,on_click=SettingsMenu)
MainMenuQuit=Button(text='Quit to desktop',scale_y=.1,scale_x=.2,color=color.clear,hightlight_color=color.clear,x=-.7,y=-.4,on_click=application.quit)
MainMenuSelector=Button(text='Level Selector',scale_y=.1,scale_x=.2,color=color.clear,hightlight_color=color.clear,x=-.7,y=-.25,on_click=LevelSelector)

#Audio loading
app.taskMgr.add(LoadAudio(path="assets/audio/settings.ogg",name="SettingsMusic",loop=True))
app.taskMgr.add(LoadAudio(path="assets/audio/ambient.ogg",name="AmbientSound1",autoplay=True,loop=True))


def load_func():
    camera.overlay.color = color.black
    logo = Sprite(name='ursina_splash', parent=camera.ui, texture='assets/textures/menu_picture.jpg', world_z=camera.overlay.z-1, scale_y=.095,scale_x=.08, color=color.clear)
    logo.animate_color(color.white, duration=2, delay=3, curve=curve.out_quint_boomerang)
    camera.overlay.animate_color(color.clear, duration=1, delay=6)
    destroy(logo, delay=5)

    def splash_input(key):
        destroy(logo)
        camera.overlay.animate_color(color.clear, duration=.25)

    logo.input = splash_input
load_func()
app.run()