import time
import pickle
import azure.cognitiveservices.speech as speechsdk
import numpy
from moviepy.editor import VideoFileClip
import os
from pathlib import Path
import azure.functions as func
import requests
import azure.cognitiveservices.speech as speechsdk




# Create the Audio File from Video to extract text
def createAudiofile(videoFile):
    video = VideoFileClip(videoFile)
    audio = video.audio
    audio.set_duration(video.duration)
    targetpath = f"{str(os.path.dirname(videoFile))}\\audio\\{Path(videoFile).stem}.wav"    
    audio.write_audiofile(targetpath) 
    return targetpath


def transcribeVideoFile(videofile):
    result = ()
    audiofile = createAudiofile(videofile)
    subscriptionKey = "8b55e73608b74816949046c46a09c0c6" #os.environ["speechSubscriptionKey"]#
    speech_region = os.environ["speechRegion"] #"westus"
    speech_config = speechsdk.SpeechConfig(subscriptionKey, speech_region)
    speech_config.speech_recognition_language=os.environ["speechLanguage"] #"en-US"
    audio_config = speechsdk.audio.AudioConfig(filename=audiofile)
    speech_recogniser = speechsdk.SpeechRecognizer(speech_config,audio_config)


    def recognised(evt):
        recognised_text = evt.result.text
        result.append(recognised_text)

    def stop_cb(evt):
        print(f"Closing in {evt}")
        speech_recogniser.stop_continuous_recognition()
        global done
        done= True
        print(f"Closed on {evt}")
    while not done:
        time.sleep(0.5)
    # dump the transcribed file to  
    with open ("transcribed_video.pickle","wb") as f:
        pickle.dump()
        print("Transcription Dumped")

def main(myblob: func.InputStream):
    
    createAudiofile(videoFile="C:\\Users\\rakesh.khanna\\Downloads\\TestAudio\\Qualtrics.mp4")

if __name__ == "__main__":
    main()