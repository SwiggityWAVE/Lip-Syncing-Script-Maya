#https://towardsdatascience.com/speech-recognition-with-timestamps-934ede4234b2

from cgi import test
from re import split
import threading
from unittest import result
from vosk import Model, KaldiRecognizer, SetLogLevel
import os
import wave
import json
import time
from playsound import playsound
from threading import Thread

class Word:
    ''' A class representing a word from the JSON format for vosk speech recognition API '''

    def __init__(self, dict):
        '''
        Parameters:
          dict (dict) dictionary from JSON, containing:
            conf (float): degree of confidence, from 0 to 1
            end (float): end time of the pronouncing the word, in seconds
            start (float): start time of the pronouncing the word, in seconds
            word (str): recognized word
        '''

        self.conf = dict["conf"]
        self.end = dict["end"]
        self.start = dict["start"]
        self.word = dict["word"]

    def to_string(self):
        ''' Returns a string describing this instance '''
        return "{:20} from {:.2f} sec to {:.2f} sec, confidence is {:.2f}%".format(
            self.word, self.start, self.end, self.conf*100)

def PlaySoundOnThread(audioFileName):
    playsound(audioFileName)

def transcribeFile(audioFile):

    SetLogLevel(0)

    if not os.path.exists("model"):
        print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
        exit (1)

    #wf = wave.open("Hello World.wav", "rb")
    wf = wave.open(audioFile, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print ("Audio file must be WAV format mono PCM.")
        exit (1)

    model = Model("model")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)


    # get the list of JSON dictionaries
    results = []
    # recognize speech using vosk model
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            part_result = json.loads(rec.Result())
            results.append(part_result)
    part_result = json.loads(rec.FinalResult())
    results.append(part_result)


    # convert list of JSON dictionaries to list of 'Word' objects
    list_of_Words = []
    for sentence in results:
        if len(sentence) == 1:
            # sometimes there are bugs in recognition 
            # and it returns an empty dictionary
            # {'text': ''}
            continue
        for obj in sentence['result']:
            w = Word(obj)  # create custom Word object
            list_of_Words.append(w)  # and add it to list

    wf.close()  # close audiofile

    # output to the screen
    """"
    for word in list_of_Words:
        print(word.to_string())
    """
    return list_of_Words

class TimeLine:
        def __init__(self, fileLengthInSeconds, keyframesPerSecond):
            self.fileLengthInSeconds = fileLengthInSeconds
            self.keyframesPerSecond = int(keyframesPerSecond)
            self.finalKeyframe = round(fileLengthInSeconds * self.keyframesPerSecond)
            self.timeLine = []

            for i in range(self.finalKeyframe):
                self.timeLine.append(".")

        def ModifyTimeLine(self, list_of_Words):
            for word in list_of_Words:
                wordTimeLength = float(word.end) - float(word.start) 
                secondsPerKeyframe = wordTimeLength/len(word.word)
                
                for i in range(len(word.word)):
                    character = word.word[i]
                    keyFrameTimeStamp = round(self.keyframesPerSecond * ( word.start + (secondsPerKeyframe * i)))
                    timeLine.timeLine[keyFrameTimeStamp] = character
                
                
                
            
            


        def PlayTimeline(self):
            #playsound('Hello there.wav')
            currentKeyframe = 0
            lastPresentedKeyframe = -1
            audioThread = threading.Thread(target=PlaySoundOnThread, args=('Hello there.wav', ))
            playTimeInKeyframes = round(self.fileLengthInSeconds * self.keyframesPerSecond)
            audioThread.start()
            startTime = time.time()
            

            while(lastPresentedKeyframe < playTimeInKeyframes):
                playTime = float(time.time()) - startTime

                currentKeyframe = int(playTime * self.keyframesPerSecond)

                if(currentKeyframe > lastPresentedKeyframe and currentKeyframe < playTimeInKeyframes):
                    lastPresentedKeyframe = currentKeyframe
                    print(self.timeLine[currentKeyframe])






timeLine = TimeLine(3.1, 24)
list_of_Words = []
list_of_Words = transcribeFile("Hello there.wav")
timeLine.ModifyTimeLine(list_of_Words)
timeLine.PlayTimeline();


"""
for keyframe in timeLine.timeLine:
    print(keyframe)

for word in list_of_Words:
        print(word.to_string())

"""