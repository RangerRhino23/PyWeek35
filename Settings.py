global MainMenuQuit, MainMenuSettings, MainMenuStart, MainMenuBackground
MainMenuStart=Button(text='Resume',scale_y=.1,scale_x=.2,color=color.clear,highlight_color=color.clear,x=-.7,on_click=Return)
MainMenuSettings=Button(text='Settings',scale_y=.1,scale_x=.2,color=color.clear,hightlight_color=color.clear,x=-.7,y=-.12,on_click=SettingsMenu)
MainMenuQuit=Button(text='Quit to desktop',scale_y=.1,scale_x=.2,color=color.clear,hightlight_color=color.clear,x=-.7,y=-.4,on_click=application.quit)
MainMenuBackground=Entity(parent=camera.ui,model='quad', color=color.black, scale=1000)