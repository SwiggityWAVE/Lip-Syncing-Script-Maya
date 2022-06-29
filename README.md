# Lip-Syncing-Script-Maya

This Lip-Syncing script was created by me Adrian Björkholm for my bachellor thesis.
Please come and visit my site to see more of the stuff I have created at https://adrianbjorkholm.com/ or my github at https://github.com/SwiggityWAVE

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
