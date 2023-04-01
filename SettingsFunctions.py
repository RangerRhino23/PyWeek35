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
    global VsyncSetting,volume_slider,volume,FullscreenSetting
    MainMenuStart.disabled=True; MainMenuStart.visible=False
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

def SettingsMenuReturn():
    MainMenuSettings.on_click=SettingsMenu; MainMenuSettings.text='Settings'; MainMenuSettings.y=-.1
    MainMenuStart.disabled=False; MainMenuStart.visible=True
    destroy(VsyncSetting); destroy(volume_slider); destroy(FullscreenSetting)
    MainMenuQuit.visible=True; MainMenuQuit.disabled=False

def Return():
    global InSettings
    destroy(MainMenuSettings); destroy(MainMenuStart); destroy(MainMenuQuit); destroy(MainMenuBackground)
    InSettings=False
