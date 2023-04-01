from ursina import *

app = Ursina()

# create scrolling text
scrolled_text = []
scroll_text1 = Text(text='This marks the end of the game.', font='assets/misc/Starjedi.ttf', origin=(0,0), y=-.8, scale=2)
scrolled_text.append(scroll_text1)
scroll_text2 = Text(text='This was our pyweek35 game.', font='assets/misc/Starjedi.ttf', origin=(0,0), y=-1, scale=2)
scrolled_text.append(scroll_text2)
scroll_text3 = Text(text='Github: https://github.com/RangerRhino23/Pyweek35', font='assets/misc/Starjedi.ttf', origin=(0,0), y=-1.2, scale=2)
scrolled_text.append(scroll_text3)
scroll_text4 = Text(text="And we'd like to thank you for playing", font='assets/misc/Starjedi.ttf', origin=(0,0), y=-1.4, scale=2)
scrolled_text.append(scroll_text4)
scroll_text5 = Text(text='We hope you had an amazing time.', font='assets/misc/Starjedi.ttf', origin=(0,0), y=-1.6, scale=2)
scrolled_text.append(scroll_text5)
scroll_text6 = Text(text='Thank you so much! and goodbye.', font='assets/misc/Starjedi.ttf', origin=(0,0), y=-1.8, scale=2)
scrolled_text.append(scroll_text6)

scroll_speed = 0.05

# update the y position of the text objects over time
def update():
    for text in scrolled_text:
        text.y += time.dt * scroll_speed
        if text.y >= 1.6:
            destroy(text)
    if not scrolled_text:
        application.close()

app.run()
