#https://towardsdatascience.com/speech-recognition-with-timestamps-934ede4234b2

from cgi import test
from re import split
from unittest import result
from vosk import Model, KaldiRecognizer, SetLogLevel
import eng_to_ipa as p
import os
import wave
import json
#import time
#from playsound import playsound
#from threading import Thread
#import threading

"""
def PlaySoundOnThread(audioFileName):
    playsound(audioFileName)
"""

audioFile = "D:\Github\Python LipsyncScript\LipsyncingScriptRepository\Lip-Syncing-Script-Maya\PythonLipSyncScriptWorkSpace\Hello there.wav"
voskModelPath =  "D:\Github\Python LipsyncScript\model"

SetLogLevel(0)

if 'model' not in globals():
    print("Loading model...")
    if not os.path.exists(voskModelPath):
        print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
        exit (1)
    model = Model(voskModelPath)
print("Model is loaded")




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

def transcribeFile(audioFile, model):

    wf = wave.open(audioFile, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print ("Audio file must be WAV format mono PCM.")
        exit (1)

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
    return list_of_Words

def ConvertEnglishToIpa(list_of_Words):
    for i in range(len(list_of_Words)):
        ipaWord = p.convert(list_of_Words[i].word)
        list_of_Words[i].word = ipaWord


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
                
        """      
        def PlayTimeline(self):
            #Audio, thread and time
            #audioThread = threading.Thread(target=PlaySoundOnThread, args=('D:\Github\Python LipsyncScript\LipsyncingScriptRepository\Lip-Syncing-Script-Maya\PythonLipSyncScriptWorkSpace\Hello there.wav'))
            #audioThread.start()


            currentKeyframe = 0
            lastPresentedKeyframe = -1
            playTimeInKeyframes = round(self.fileLengthInSeconds * self.keyframesPerSecond)
            startTime = time.time()
            

            while(lastPresentedKeyframe < playTimeInKeyframes - 1):
                playTime = float(time.time()) - startTime

                currentKeyframe = round(playTime * self.keyframesPerSecond)

                if(currentKeyframe > lastPresentedKeyframe):
                    lastPresentedKeyframe = currentKeyframe
                    print(self.timeLine[currentKeyframe])
        """


timeLine = TimeLine(3.1, 24)
list_of_Words = []
list_of_Words = transcribeFile(audioFile, model)
ConvertEnglishToIpa(list_of_Words)
timeLine.ModifyTimeLine(list_of_Words)
#timeLine.PlayTimeline();


for c in timeLine.timeLine:
    print(c)

print("Run completed\n")
