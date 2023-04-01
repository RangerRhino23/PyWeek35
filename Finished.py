from ursina import *

app = Ursina()

# create scrolling text
scroll_text1 = Text(text='This marks the end of the game.', font='assets/misc/Starjedi.ttf', origin=(0,0), y=-.8, scale=2)
scroll_text2 = Text(text='This was our pyweek35 game.', font='assets/misc/Starjedi.ttf', origin=(0,0), y=-1, scale=2)
scroll_text3 = Text(text="And we'd like to thank you for playing.", font='assets/misc/Starjedi.ttf', origin=(0,0), y=-1.2, scale=2)
scroll_text4 = Text(text='We hope you had an amazing time.', font='assets/misc/Starjedi.ttf', origin=(0,0), y=-1.4, scale=2)
scroll_text5 = Text(text='Thank you so much! and goodbye.', font='assets/misc/Starjedi.ttf', origin=(0,0), y=-1.6, scale=2)

# update the y position of the text objects over time
def update():
    scroll_text1.y += time.dt * 0.05  # adjust speed as needed
    if scroll_text1.y > 0.9:
        scroll_text1.y = 0.9

    scroll_text2.y += time.dt * 0.05
    if scroll_text2.y > 0.9:
        scroll_text2.y = 0.9

    scroll_text3.y += time.dt * 0.05
    if scroll_text3.y > 0.9:
        scroll_text3.y = 0.9

    scroll_text4.y += time.dt * 0.05
    if scroll_text4.y > 0.9:
        scroll_text4.y = 0.9

    scroll_text5.y += time.dt * 0.05
    if scroll_text5.y > 0.9:
        scroll_text5.y = 0.9

app.run()
