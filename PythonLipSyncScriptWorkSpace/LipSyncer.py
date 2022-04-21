#https://towardsdatascience.com/speech-recognition-with-timestamps-934ede4234b2

from asyncio.windows_events import NULL
from cgi import test
from re import split
from unittest import result
from vosk import Model, KaldiRecognizer, SetLogLevel
import eng_to_ipa as p
import os
import wave
import json
import contextlib



from PySide2 import QtCore, QtWidgets
import pymel.core as pm

"""
#REJECTION CORNER


#import time
#from playsound import playsound
#from threading import Thread
#import threading


def PlaySoundOnThread(audioFileName):
    playsound(audioFileName)
"""



"""#Reimport This"""



filePathKeys = ["audioFile", "voskModel", "config"]
filePaths = {"audioFile" : "something.wav", "voskModel" : "ModelPath", "config" : "ConfigPath"}
keyframesPerSecond = 24
audioFileLength = 0
#audioFile = "D:\Github\Python LipsyncScript\LipsyncingScriptRepository\Lip-Syncing-Script-Maya\PythonLipSyncScriptWorkSpace\Hello there.wav"
#voskModelPath =  "D:\Github\Python LipsyncScript\model"

f = open("D:\Github\Python LipsyncScript\LipsyncingScriptRepository\Lip-Syncing-Script-Maya\PythonLipSyncScriptWorkSpace\LipSyncerConfig.txt", "r")
filePaths["voskModel"] = f.readline().replace('\n', '')
filePaths["audioFile"] = f.readline().replace('\n', '')
f.close()

SetLogLevel(0)

if 'model' not in globals():
    print("Loading model...")
    if not os.path.exists(filePaths["voskModel"]):
        print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
        exit (1)
    model = Model(filePaths["voskModel"])
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
            print(part_result)
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

def CheckAudioFileLength():
    #https://stackoverflow.com/questions/7833807/get-wav-file-length-or-duration
    fname = filePaths["audioFile"]
    with contextlib.closing(wave.open(fname,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration

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
                    self.timeLine[keyFrameTimeStamp] = character
                
def animateMesh(timeLine):
    print("This animations has ", len(timeLine.timeLine), " frames")
    for keyframe in range(len(timeLine.timeLine)):
        #print(timeLine.timeLine[keyframe])
        #pm.currentTime(keyframe)

        if timeLine.timeLine[keyframe] == '.':
            print("DOT")
            pm.setKeyframe(visemeNodes["aa"], at='weight[0]', v=0, t=keyframe)
        else:
            print("NOT DOT")
            pm.setKeyframe(visemeNodes["aa"], at='weight[0]', v=1, t=keyframe)

def RunScript():
    BindVisemeNodes()
    audioFileLength = CheckAudioFileLength()
    timeLine = TimeLine(audioFileLength, keyframesPerSecond)
    list_of_Words = []
    list_of_Words = transcribeFile(filePaths["audioFile"], model)
    ConvertEnglishToIpa(list_of_Words)
    timeLine.ModifyTimeLine(list_of_Words)
    animateMesh(timeLine)
    print("Task completed")

    

#RunScript()

##UI and Pymel##


def ChangeFilePathForAudioFile():
    newPath = pm.fileDialog2(fileFilter="*.wav")
    filePaths["audioFile"] = str(newPath[0])
    filePathQLineEdit[0].setText(filePaths["audioFile"])
    CheckAudioFileLength()
    
    
    
def ChangeFilePathForModel():
    newPath = pm.fileDialog2(fm=2, fileFilter="*.:")
    filePaths["voskModel"] = str(newPath[0])
    filePathQLineEdit[1].setText(filePaths["voskModel"])
    
def ChangeFilePathForConfig():
    filePathQLineEdit[2].setText("NOT WORKING")


#MAIN LOOP
wid = QtWidgets.QWidget()
wid.resize(1024, 1024)
wid.setWindowTitle("Window")

#File system

filePathQLineEdit = []
changeFilePathQPushButton = []
filePathLabel = []

index = 0
for key in filePathKeys:
    filePathLabel.append(QtWidgets.QLabel(wid))
    filePathLabel[index].setText(filePathKeys[index])
    filePathLabel[index].move(256, 48 * index)
    
    filePathQLineEdit.append(QtWidgets.QLineEdit(filePaths[key], parent = wid))
    filePathQLineEdit[index].move(312, 48 * index)
    
    changeFilePathQPushButton.append(QtWidgets.QPushButton('ChangeFilePath', parent = wid))
    changeFilePathQPushButton[index].move(456, 48 * index)
    index += 1
    
changeFilePathQPushButton[0].clicked.connect(ChangeFilePathForAudioFile)
changeFilePathQPushButton[1].clicked.connect(ChangeFilePathForModel)
changeFilePathQPushButton[2].clicked.connect(ChangeFilePathForConfig)



RunScriptQPushButton = QtWidgets.QPushButton('Run Script', parent = wid)
RunScriptQPushButton.move(512, 48 * index)
RunScriptQPushButton.clicked.connect(RunScript)

UndoQPushButton = QtWidgets.QPushButton('Undo', parent = wid)
UndoQPushButton.move(512, 56 * index)
UndoQPushButton.clicked.connect(pm.undo)



#Viseme System
#Lists all blendshapes in scene
blendShapes = pm.general.ls(exactType = "blendShape")
blendShapesAsString = []
for blendshape in blendShapes:
    blendShapesAsString.append(str(blendshape))


visemeList = ["Silent", "PP", "FF", "TH", "DD", "kk", "CH", "SS", "nn", "RR", "aa", "E", "I", "O", "U"]
visemeLabel = []
visemeQComboBox = []
visemeNodes = {"Silent" : NULL, "PP" : NULL, "FF" : NULL, "TH" : NULL, "DD" : NULL, "kk" : NULL, "CH" : NULL, "SS" : NULL, "nn" : NULL, "RR" : NULL, "aa" : NULL, "E" : NULL, "I": NULL, "O" : NULL, "U": NULL}


def BindVisemeNodes():
    index = 0
    for viseme in visemeList:
        visemeNodes[viseme] = visemeQComboBox[index].currentText() + '.envelope'
        index += 1
    
        


index = 0
for viseme in visemeList:
    visemeLabel.append(QtWidgets.QLabel(wid))
    visemeLabel[index].setText(visemeList[index] + ": ")
    visemeLabel[index].move(0, 48 * index)
    
    visemeQComboBox.append(QtWidgets.QComboBox(wid))
    visemeQComboBox[index].addItems(blendShapesAsString)
    visemeQComboBox[index].move(visemeLabel[index].width(), 48 * index)
    
    
    index += 1





############################################
"""
dropDown = QtWidgets.QComboBox(wid)
dropDown.addItems(blendShapesAsString)
dropDown.move(dropDownLabel.width(), 0)
"""



wid.show()

"""
#Execute mainProgram
executeButton = QtWidgets.QPushButton('testFunc', parent = wid)
executeButton.resize(128, 32)
executeButton.move(20, 20)
executeButton.clicked.connect(runMainProgram)
"""