#!/usr/bin/python3

from gtts import gTTS

intext=("Please face the camera.   A photograph will be taken and sent to a member of staff.  You will then be given further instructions.  Thank you for your patience.") 
lang='en'
filename = 'outtext.mp3'  

tts = gTTS(text=intext, lang='en') 
tts.save(filename)