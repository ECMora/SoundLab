#import pyglet
#window = pyglet.window.Window()
#label = pyglet.text.Label('Hello, world',font_name='Times New Roman',font_size=36,x=window.width//2, y=window.height//2,anchor_x='center', anchor_y='center')
#image=pyglet.resource.image('a.jpg')
#audio=pyglet.media.Player()
#source=pyglet.media.load("1.wav")
#audio.queue(source)
#audio.play()
#
#@window.event
#def on_draw():
#    window.clear()
#    image.blit(0,0,width=400,height=400)
#
#
#pyglet.app.run()
import random

file=open("names.txt","rb")
users=file.readlines()

people=range(len(users))
peopletaken=[]

for i in range(len(people)):
    peopletaken.append(False)

gifts=[]
iter=0
error=True
while(error):
    error=False
    iter+=1
    for i in range(len(people)):
        me=peopletaken[i]
        peopletaken[i]=True
        candidates=[x for x in people if not peopletaken[x]]
        if(len(candidates)==0):
            error=True
            gifts=[]
            peopletaken=[False for x in peopletaken]
            break
        chosen=random.randrange(len(candidates))
        peopletaken[candidates[chosen]]=True
        gifts.append((i,candidates[chosen]))
        peopletaken[i]=me


for user_from,user_to in gifts:
    print(str(users[user_from])+" le regala a "+str(users[user_to]))

