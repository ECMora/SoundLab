#import pyglet
#
#audio=pyglet.media.ManagedSoundPlayer()
#audio.queue(pyglet.media.load("1.wavate"))
#audio.play()

import pyaudio
import wave
import time
import sys

wf = wave.open("54.wav", 'rb')

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# define callback (2)
def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    return (data, pyaudio.paContinue)

# open stream using callback (3)
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                stream_callback=callback)

# start the stream (4)
stream.start_stream()

# wait for stream to finish (5)
while stream.is_active():
    time.sleep(0.1)

# stop stream (6)
stream.stop_stream()
stream.close()
wf.close()

# close PyAudio (7)
p.terminate()


#import random

#file=open("names.txt","rb")
#users=file.readlines()
#
#people=range(len(users))
#peopletaken=[]
#
#for i in range(len(people)):
#    peopletaken.append(False)
#
#gifts=[]
#iter=0
#error=True
#while(error):
#    error=False
#    iter+=1
#    for i in range(len(people)):
#        me=peopletaken[i]
#        peopletaken[i]=True
#        candidates=[x for x in people if not peopletaken[x]]
#        if(len(candidates)==0):
#            error=True
#            gifts=[]
#            peopletaken=[False for x in peopletaken]
#            break
#        chosen=random.randrange(len(candidates))
#        peopletaken[candidates[chosen]]=True
#        gifts.append((i,candidates[chosen]))
#        peopletaken[i]=me
#
#
#for user_from,user_to in gifts:
#    print(str(users[user_from])+" le regala a "+str(users[user_to]))
#
