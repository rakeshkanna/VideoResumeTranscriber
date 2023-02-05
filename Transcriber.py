import time
import pickle
import azure.cognitiveservices.speech as speechsdk
from moviepy.editor import VideoFileClip
import os
from pathlib import Path
import azure.functions as func
import azure.cognitiveservices.speech as speechsdk


done = False
# Create the Audio File from Video to extract text
def createAudiofile(videoFile):
    video = VideoFileClip(videoFile)
    audio = video.audio
    audio.set_duration(video.duration)
    targetpath = f"{str(os.path.dirname(videoFile))}\\audio\\{Path(videoFile).stem}.wav"    
    audio.write_audiofile(targetpath) 
    return targetpath


def transcribeVideoFile(videofile):
    global done 
    done = False
    result = ()
    audiofile = createAudiofile(videofile)
    subscriptionKey = "8b55e73608b74816949046c46a09c0c6" #os.environ["speechSubscriptionKey"]#
    speech_region =  "westus"
    speech_config = speechsdk.SpeechConfig(subscriptionKey, speech_region)
    speech_config.speech_recognition_language= "en-US"
    audio_config = speechsdk.audio.AudioConfig(filename=audiofile)
    speech_recogniser = speechsdk.SpeechRecognizer(speech_config,audio_config)
    targetPath = f"{str(os.path.dirname(videofile))}\\Text\\{Path(videofile).stem}.txt"

    def recognised(evt):
        recognised_text = evt.result.text
        print(recognised_text)
        with open(targetPath, "a") as f:
            f.write(recognised_text+'\n')


    def stop_cb(evt):
        print(f"Closing in {evt}")
        global done
        done= True
        print(f"Closed on {evt}")
    speech_recogniser.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recogniser.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recogniser.canceled.connect(stop_cb)
    speech_recogniser.recognized.connect(recognised)
    speech_recogniser.start_continuous_recognition()
    
    while not done:
        time.sleep(0.5)
    # dump the transcribed file to  
    
    speech_recogniser.stop_continuous_recognition()
