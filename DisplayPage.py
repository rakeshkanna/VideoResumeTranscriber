import datetime
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image, ImageOps
from tkVideoPlayer import TkinterVideo
from tkinter import *
import Transcriber as transcriber

def update_duration(event):
    """ updates the duration after finding the duration """
    duration = vid_player.video_info()["duration"]
    end_time["text"] = str(datetime.timedelta(seconds=duration))
    progress_slider["to"] = duration

def update_scale(event):
    """ updates the scale value """
    progress_value.set(vid_player.current_duration())

def load_video():
    """ loads the video """
    file_path = filedialog.askopenfilename(filetypes=[("Video files", ".mp4"),("All Files","*.*")] ) 

    if file_path:
        strFile.set(file_path)

def seek(value):
    """ used to seek a specific timeframe """
    vid_player.seek(int(value))

def skip(value: int):
    """ skip seconds """
    vid_player.seek(int(progress_slider.get())+value)
    progress_value.set(progress_slider.get() + value)

def play_pause():
    """ pauses and plays """
    if vid_player.is_paused():
        vid_player.play()
        play_pause_btn["text"] = "Pause"

    else:
        vid_player.pause()
        play_pause_btn["text"] = "Play"

def video_ended(event):
    """ handle video ended """
    progress_slider.set(progress_slider["to"])
    play_pause_btn["text"] = "Play"
    progress_slider.set(0)

def transcribeVideo():
    if strFile.get():
        resume_transcribed_text = transcriber.transcribeVideoFile(strFile.get())
        resume_text.insert(tk.END,resume_transcribed_text)
    else:
        resume_text.insert(tk.END,"FileNotFound")
    
def getEntities():
    entities_text.insert(tk.END,"Entities")

root = tk.Tk()
root.title("Resume Parser")
root.minsize(900,600)
left_frame = Frame(root,width=200,height=400)
left_frame.grid(row=0,column=0,padx=10,pady=5)
strFile = tk.StringVar()
right_frame = Frame(root, width=650, height=400)
right_frame.grid(row=0, column=1, padx=10, pady=5)

txtFile = tk.Entry(left_frame, width=20,textvariable=strFile).grid(row=0,column=0,padx=5,pady=5)
resume_label = Label(right_frame,width=25,text="Text",font="comicsansms 30 bold",fg="black").pack()
resume_text = Text(right_frame,width=50,height=10,font=("Helvetica", 16))
resume_text.pack()
entities_label = Label(right_frame,width=25,text="Entities",font="comicsansms 30 bold",fg="black").pack()
entities_text=Text(right_frame,width=50,height=10,font=("Helvetica", 16))
entities_text.pack(fill=X)
load_btn = tk.Button(left_frame, text="Load", command=load_video).grid(row=0,column=1,padx=5,pady=5)
textconvert_btn = tk.Button(left_frame, text="GenerateText", command=transcribeVideo).grid(row=1,column=0,padx=5,pady=5)
ner_btn = tk.Button(left_frame, text="IdentifyEntities", command=getEntities).grid(row=2,column=0,padx=5,pady=5)
# vid_player = TkinterVideo(scaled=True, master=right_frame)
# vid_player.pack(expand=True, fill="both")

# play_pause_btn = tk.Button(right_frame, text="Play", command=play_pause)
# play_pause_btn.pack()

# skip_plus_5sec = tk.Button(right_frame, text="<-5", command=lambda: skip(-5))
# skip_plus_5sec.pack(side="left")

# start_time = tk.Label(right_frame, text=str(datetime.timedelta(seconds=0)))
# start_time.pack(side="left")

# progress_value = tk.IntVar(right_frame)

# progress_slider = tk.Scale(right_frame, variable=progress_value, from_=0, to=0, orient="horizontal", command=seek)
# progress_slider.bind("<ButtonRelease-1>", seek)
# progress_slider.pack(side="left", fill="x", expand=True)

# end_time = tk.Label(right_frame, text=str(datetime.timedelta(seconds=0)))
# end_time.pack(side="left")

# vid_player.bind("<<Duration>>", update_duration)
# vid_player.bind("<<SecondChanged>>", update_scale)
# vid_player.bind("<<Ended>>", video_ended )

# skip_plus_5sec = tk.Button(right_frame, text="->5", command=lambda: skip(5))
# skip_plus_5sec.pack(side="left")


root.mainloop()