"""
This Lip-Syncing script was created by me Adrian Björkholm for my bachellor thesis.
Please come and visit my site to see more of the stuff I have created https://adrianbjorkholm.com/ or my github at https://github.com/SwiggityWAVE

Word class and the "transcribeFile" is inspiered by this code example:
    https://towardsdatascience.com/speech-recognition-with-timestamps-934ede4234b2

BEFORE RUNNING THE SCRIPT:

INSTALLATION GUIDE:
    Vosk, https://alphacephei.com/vosk/install
    eng-to-ipa, https://pypi.org/project/eng-to-ipa/

    To succesfully install the packages you might need to update your Package manager (pip3) inside of Maya.
    The following link is instructions on how to install Python packages for Maya:
    https://knowledge.autodesk.com/support/maya/learn-explore/caas/CloudHelp/cloudhelp/2022/ENU/Maya-Scripting/files/GUID-72A245EC-CDB4-46AB-BEE0-4BBBF9791627-htm.html
    
Instructions:
    This lip syncing script uses the Oculus documentation ( https://developer.oculus.com/documentation/unity/audio-ovrlipsync-viseme-reference/ )
    as references of what visemes are being used. Bind the prefered blendshape to the correct viseme.


    The file format needs to be .wav and only have one channel in mono. The script does not support stereo sound.
    The audio file needs to be formatted to PCM. If the audiofile has the wrong configurations Maya might crash so make sure to save your scene before you run the script.

    A voice transcription model needs to be attached to the script. You can download one here -> https://alphacephei.com/vosk/models
    It's recommended only to generate lipsync animations in English because the transcription to phonetics conversion
    the library is limited to only supporting English.

    The keyframes per second box need to have the same value as the animation timelines framerate.
    The "Silence Time-Criteria" and "Silence Cut-Down" boxes are configurable to the animator's preference.
    "Silence Time-Criteria" keeps track of how long the silence is between the said words in the audio file and will give 
    the mesh instructions to close the mouth between the words depending on how long the silence is between the words.
    "Silence Cut-Down" determines how much time it will take for the mesh to close its mouth since the silence was initiated.

    If the blendshapes that are meant to be used were created after the script was loaded, you have to reload the script



"""

from asyncio.windows_events import NULL
from cgi import test
from pyexpat import model
from re import split
from unittest import result
from vosk import Model, KaldiRecognizer, SetLogLevel
import eng_to_ipa as p
import os
import wave
import json
import contextlib



from PySide2 import QtCore, QtWidgets

alertWid = QtWidgets.QWidget()
alertWid.resize(512, 64)
alertWid.setWindowTitle("Program is loading")
alertWid.show()

import pymel.core as pm

filePathKeys = ["audioFile", "voskModel", "config"]
filePaths = {"audioFile" : "", "voskModel" : "", "config" : ""}
silenceTimeCriteria = 5/24
silenceCutDown = 3/24
keyframesPerSecond = 24
audioFileLength = 0
#audioFile = "D:\Github\Python LipsyncScript\LipsyncingScriptRepository\Lip-Syncing-Script-Maya\PythonLipSyncScriptWorkSpace\Hello there.wav"
#voskModelPath =  "D:\Github\Python LipsyncScript\model"



"""Config file text data"""
#f = open("D:\Github\Python LipsyncScript\LipsyncingScriptRepository\Lip-Syncing-Script-Maya\PythonLipSyncScriptWorkSpace\LipSyncerConfig.txt", "r")
#filePaths["voskModel"] = f.readline().replace('\n', '')
#filePaths["audioFile"] = f.readline().replace('\n', '')
#f.close()

SetLogLevel(0)



"""
if 'model' not in globals():
    print("Loading model...")
    if not os.path.exists(filePaths["voskModel"]):
        print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
        exit (1)
    model = Model(filePaths["voskModel"])
print("Model is loaded")
"""

alertWid.close()

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
            self.silenceTimeLine = []

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

            nrOfWords = len(list_of_Words)
            for index in range(nrOfWords):
                silenceTimeStamp = []
                if(nrOfWords == 1):
                    silenceTimeStamp = [0, list_of_Words[index].start]
                    self.silenceTimeLine.append(silenceTimeStamp)

                    silenceTimeStamp = [list_of_Words[index].end, audioFileLength]
                    self.silenceTimeLine.append(silenceTimeStamp)

                elif (index == 0):
                    silenceTimeStamp = [0, list_of_Words[index].start]
                    self.silenceTimeLine.append(silenceTimeStamp)
                elif (index == nrOfWords - 1):
                    silenceTimeStamp = [list_of_Words[index].end, audioFileLength]
                    self.silenceTimeLine.append(silenceTimeStamp)
                else:
                    silenceTimeStamp = [list_of_Words[index].end, list_of_Words[index + 1].start]

                silenceTimeStamp[0] += silenceCutDown
                silenceTimeStamp[1] -= silenceCutDown

                
                if((silenceTimeStamp[1] - silenceTimeStamp[0]) >= silenceTimeCriteria):
                    self.silenceTimeLine.append(silenceTimeStamp)


                
def animateMesh(timeLine):
    print("This animations has ", len(timeLine.timeLine), " frames")
    undefinedChars = []
    for keyframe in range(len(timeLine.timeLine)):

        if timeLine.timeLine[keyframe] != '.':

            for visme in visemeList:
                pm.setKeyframe(visemeNodes[visme], at='weight[0]', v=0, t=keyframe)

            case = timeLine.timeLine[keyframe]
            #["Silent", "PP", "FF", "TH", "DD", "kk", "CH", "SS", "nn", "RR", "aa", "E", "I", "O", "U"]


            if (case == 'ɓ') or (case == 'ɱ') or (case == 'ɯ') or (case == 'ɰ') or (case == 'ʘ') or (case == 'p') or (case == 'b') or (case == 'm'):
                #Viseme:    PP                       Phonemes:      p, b, m                         Word example:           put, bat, mat
                print("1")
                pm.setKeyframe(visemeNodes["PP"], at='weight[0]', v=1, t=keyframe)

            elif (case == 'β') or (case == 'φ') or (case == 'ɸ') or (case == 'ʋ') or (case == 'ʍ') or (case == 'ŵ') or (case == 'ɯ') or (case == 'ɰ') or (case == 'ŵ') or (case == 'ẃ') or (case == 'f') or (case == 'v'):
                #Viseme:    FF                       Phonemes:      f, v                            Word example:           fat, vat
                print("2")
                pm.setKeyframe(visemeNodes["FF"], at='weight[0]', v=1, t=keyframe)

            elif (case == 'ð') or (case == 'θ') or (case == 'þ') or (case == 'w') or (case == 'ʷ'):
                #Viseme:    TH                       Phonemes:      th                              Word example:           think, that
                print("3")
                pm.setKeyframe(visemeNodes["TH"], at='weight[0]', v=1, t=keyframe)

            elif (case == 'ɖ') or (case == 'ḍ') or (case == 'ɗ') or (case == 'ʄ') or (case == 'ʈ') or (case == 'ṭ') or (case == 'd') or (case == 't') or (case == '') or (case == ''):
                #Viseme:    DD                       Phonemes:      t, d                            Word example:           tip, doll
                print("4")
                pm.setKeyframe(visemeNodes["DD"], at='weight[0]', v=1, t=keyframe)

            elif (case == 'ɟ') or (case == 'γ') or (case == 'ɣ') or (case == 'ɠ') or (case == 'ǰ') or (case == 'ʝ') or (case == 'ʲ') or (case == 'ʲ') or (case == 'ɟ') or (case == 'ɥ') or (case == 'ŷ') or (case == 'y') or (case == 'ɰ') or (case == 'ỹ') or (case == 'ȳ') or (case == 'k') or (case == 'g') or (case == 'j') or (case == 'q')or (case == 'x'):
                #Viseme:    kk                       Phonemes:      k, g                            Word example:           call, gas
                print("5")
                pm.setKeyframe(visemeNodes["kk"], at='weight[0]', v=1, t=keyframe)

            elif (case == 'ç') or (case == 'č') or (case == 'ʃ') or (case == 'ʂ') or (case == 'χ') or (case == 'c'):
                #Viseme:    CH                       Phonemes:      tS, dZ, S                       Word example:           chair, join, she
                print("6")
                pm.setKeyframe(visemeNodes["CH"], at='weight[0]', v=1, t=keyframe)

            elif (case == 'ɕ') or (case == 'š') or (case == 'ś') or (case == 'ṣ') or (case == 'ẓ') or (case == 'ʒ') or (case == 'ž') or (case == 'ʑ') or (case == 'ʐ') or (case == 's') or (case == 'z'):
                #Viseme:    SS                       Phonemes:      s, z                            Word example:           sir, zeal
                print("7")
                pm.setKeyframe(visemeNodes["SS"], at='weight[0]', v=1, t=keyframe)

            elif (case == 'ɫ') or (case == 'l') or (case == 'λ') or (case == 'ɭ') or (case == 'ʎ') or (case == 'ɭ') or (case == 'ḷ') or (case == 'ɬ') or (case == 'ɮ') or (case == 'ñ') or (case == 'ŋ') or (case == 'ɲ') or (case == 'ɳ') or (case == 'ṇ') or (case == 'n') or (case == 'l'):
                #Viseme:    nn                       Phonemes:      n, l                            Word example:           lot, not
                print("8")
                pm.setKeyframe(visemeNodes["nn"], at='weight[0]', v=1, t=keyframe)

            elif (case == 'ɹ') or (case == 'r') or (case == 'ʁ') or (case == 'ř') or (case == 'ɾ') or (case == 'ɽ') or (case == 'ṛ') or (case == 'ɻ'):
                #Viseme:    RR                       Phonemes:      r                               Word example:           red
                print("9")
                pm.setKeyframe(visemeNodes["RR"], at='weight[0]', v=1, t=keyframe)

            elif (case == 'æ') or (case == 'ɑ') or (case == 'ɐ') or (case == 'ɒ') or (case == 'α') or (case == 'ã') or (case == 'ă') or (case == 'ʌ') or (case == 'a'):
                #Viseme:    aa                       Phonemes:      A:                              Word example:           car
                print("10")
                pm.setKeyframe(visemeNodes["aa"], at='weight[0]', v=1, t=keyframe)

            elif (case == 'ə') or (case == 'ε') or (case == 'ɛ') or (case == 'ẹ') or (case == 'ɜ') or (case == 'ɚ') or (case == 'ɘ') or (case == 'ẽ') or (case == 'ĕ') or (case == 'e'):
                #Viseme:    E                       Phonemes:      e                                Word example:           bed
                print("11")
                pm.setKeyframe(visemeNodes["E"], at='weight[0]', v=1, t=keyframe)

            elif (case == 'ɪ') or (case == 'i') or (case == 'ɨ') or (case == 'ĩ') or (case == 'ĭ') or (case == '') or (case == '') or (case == '') or (case == '') or (case == 'i'):
                #Viseme:    I                       Phonemes:      ih                               Word example:           tip
                print("12")
                pm.setKeyframe(visemeNodes["I"], at='weight[0]', v=1, t=keyframe)

            elif (case == 'ħ') or (case == 'ɦ') or (case == 'h') or (case == 'ʰ') or (case == 'ɥ') or (case == 'ḥ') or (case == 'ɧ') or (case == 'ø') or (case == 'œ') or (case == 'œ') or (case == 'œ') or (case == 'ö') or (case == 'ɔ') or (case == 'ọ') or (case == 'ɵ') or (case == 'õ') or (case == 'ŏ') or (case == 'o'):
                #Viseme:    O                       Phonemes:      oh                               Word example:           toe
                print("13")
                pm.setKeyframe(visemeNodes["O"], at='weight[0]', v=1, t=keyframe)

            elif (case == 'ʊ') or (case == 'ü') or (case == 'u') or (case == 'ʉ') or (case == 'ɞ') or (case == 'ũ') or (case == 'ŭ') or (case == 'u'):
                #Viseme:    U                       Phonemes:      ou                               Word example:           book
                print("14")
                pm.setKeyframe(visemeNodes["U"], at='weight[0]', v=1, t=keyframe)

            else:
                print("character is undefined")
                undefinedChars.append(case)
    
    print("undefined Chars: ")

    for c in undefinedChars:
        print(c)

    for sil in timeLine.silenceTimeLine:
        silStart = round(sil[0]*keyframesPerSecond)
        silEnd = round(sil[1]*keyframesPerSecond)

        for visme in visemeList:
                pm.setKeyframe(visemeNodes[visme], at='weight[0]', v=0, t=silStart)
        
        for visme in visemeList:
                pm.setKeyframe(visemeNodes[visme], at='weight[0]', v=0, t=silEnd)
        
        pm.setKeyframe(visemeNodes["Silent"], at='weight[0]', v=1, t=silStart)
        pm.setKeyframe(visemeNodes["Silent"], at='weight[0]', v=1, t=silEnd)




        


def RunScript():
    global silenceTimeCriteria
    silenceTimeCriteria = float(silenceTimeCriteriaQLineEdit.text())
    global silenceCutDown
    silenceCutDown = float(silenceCutDownQLineEdit.text())
    keyframesPerSecond = float(keyframesPerSecondQLineEdit.text())

    BindVisemeNodes()
    audioFileLength = CheckAudioFileLength()
    timeLine = TimeLine(audioFileLength, keyframesPerSecond)
    list_of_Words = []
    list_of_Words = transcribeFile(filePaths["audioFile"], model)
    ConvertEnglishToIpa(list_of_Words)
    timeLine.ModifyTimeLine(list_of_Words)
    animateMesh(timeLine)

    #if importAudioQCheckBox.isChecked() is True:
    #    pm.sound(file=filePaths["audioFile"], offset=0)


    print("Task completed")
    

    


##UI and Filepaths config


def ChangeFilePathForAudioFile():
    newPath = pm.fileDialog2(fileFilter="*.wav")
    filePaths["audioFile"] = str(newPath[0])
    filePathQLineEdit[0].setText(filePaths["audioFile"])
    CheckAudioFileLength()
    
    
    
def ChangeFilePathForModel():
    
    
    global model

    newPath = pm.fileDialog2(fm=2, fileFilter="*.:")
    filePaths["voskModel"] = str(newPath[0])
    filePathQLineEdit[1].setText(filePaths["voskModel"])





    print("Loading model...")
    alertWid = QtWidgets.QWidget()
    alertWid.resize(512, 64)
    alertWid.setWindowTitle("Loading Model...")
    alertWid.show()
    


    if not os.path.exists(filePaths["voskModel"]):
        print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
        exit (1)
    model = Model(filePaths["voskModel"])
    print("Model is loaded")


    alertWid.close()
    ##############################################################
    
def ChangeFilePathForConfig():
    filePathQLineEdit[2].setText("Read console")
    print("Adding configuration profiles has not been added to the script yet")


#MAIN LOOP
wid = QtWidgets.QWidget()
wid.resize(548, 720)
wid.setWindowTitle("Lipsyncer")

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
RunScriptQPushButton.move(458, 48 * index)
RunScriptQPushButton.clicked.connect(RunScript)

#importAudioQCheckBox = QtWidgets.QCheckBox('Import audio to scene', parent = wid)
#importAudioQCheckBox.move(256, 512)

keyframesPerSecondQLineEdit = QtWidgets.QLineEdit("24", parent = wid)
keyframesPerSecondQLineEdit.move(412, 256)
silenceTimeCriteriaQLineEdit = QtWidgets.QLineEdit(str(round(5/24, 6)), parent = wid)
silenceTimeCriteriaQLineEdit.move(412, 280)
silenceCutDownQLineEdit = QtWidgets.QLineEdit(str(round(3/24, 6)), parent = wid)
silenceCutDownQLineEdit.move(412, 304)


keyframesPerSecondLabel = QtWidgets.QLabel(wid)
keyframesPerSecondLabel.setText("Keyframes per second")
keyframesPerSecondLabel.move(256, 256)

silenceTimeCriteriaLabel = QtWidgets.QLabel(wid)
silenceTimeCriteriaLabel.setText("Silence Time-Criteria")
silenceTimeCriteriaLabel.move(256, 280)

silenceCutDownLabel = QtWidgets.QLabel(wid)
silenceCutDownLabel.setText("Silence Cut-Down")
silenceCutDownLabel.move(256, 304)

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

wid.show()