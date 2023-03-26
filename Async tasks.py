async def LoadAudio(path, name=None,autoplay=False,loop=False): #Smoothly loads audio files
    global audioname
    audioname = loader.loadSfx(path)
    
    audioname=Audio(audioname,autoplay=autoplay,loop=loop)
    globals()[name] = audioname