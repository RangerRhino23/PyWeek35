global MainMenuQuit, MainMenuSettings, MainMenuStart, MainMenuBackground
MainMenuStart=Button(text='Resume',scale_y=.3,scale_x=.6,color=color.clear,highlight_color=color.clear,x=-.7,y=.2,on_click=Return)
MainMenuStart.text_entity.scale*=3
MainMenuSettings=Button(text='Settings',scale_y=.3,scale_x=.6,color=color.clear,hightlight_color=color.clear,x=-.7,y=0,on_click=SettingsMenu)
MainMenuSettings.text_entity.scale *=3
MainMenuQuit=Button(text='Quit to desktop',scale_y=.3,scale_x=.6,color=color.clear,hightlight_color=color.clear,x=-.6,y=-.15,on_click=application.quit)
MainMenuQuit.text_entity.scale*=3
MainMenuBackground=Entity(parent=camera.ui,model='quad',texture='assets/textures/menu_picture', scale_y=1,scale_x=1.8)