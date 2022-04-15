import time

startTime = time.time()
fileLength = 1;
keyframesPerSecond = 4;
finalKeyframe = fileLength * keyframesPerSecond
timeLine = []

for x in range(finalKeyframe):
    timeLine.append("silence")

currentKeyframe = 0
lastPresentedKeyframe = -1

while(startTime + fileLength>= time.time()):
    playTime = float(time.time()) - startTime

    currentKeyframe = int(playTime * keyframesPerSecond)

    if(currentKeyframe > lastPresentedKeyframe):
        lastPresentedKeyframe = currentKeyframe
        print(timeLine[int(playTime)])
        print(currentKeyframe)
        print(playTime)
print("Time is up\n");