import datetime
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image, ImageOps
from tkVideoPlayer import TkinterVideo
from tkinter import *
import Transcriber as transcriber
from pathlib import Path
import os


def load_video():
    """ loads the video """
    file_path = filedialog.askopenfilename(filetypes=[("Video files", ".mp4"),("All Files","*.*")] ) 

    if file_path:
        strFile.set(file_path)


def transcribeVideo():
    if strFile.get():
        resume_transcribed_text = transcriber.transcribeVideoFile(strFile.get())
        resume_text.delete("1.0",tk.END)
        resume_text.insert(tk.END,resume_transcribed_text)
    else:
        resume_text.delete("1.0",tk.END)
        resume_text.insert(tk.END,"FileNotFound")
    
def getEntities():
    resumetext = resume_text.get("1.0",tk.END)
    print(resumetext)
    if resumetext and resumetext !="FileNotFound\n" and resumetext!='\n':
        entities_json = transcriber.IdentifyCustomEntities([resumetext])
    elif strFile.get():
        print("finding path")
        targetPath = f"{str(os.path.dirname(strFile.get()))}\\Text\\{Path(strFile.get()).stem}.txt"
        with open(targetPath) as f:
            resumetext = [f.read()]
        if resumetext:
            entities_json =transcriber.IdentifyCustomEntities(resumetext)
        else:
            print("Error1")
            entities_json = "Resume for Entity Recognition not found"    
    else:
        print("Error1")
        entities_json = "Resume for Entity Recognition not found"
    entities_text.delete("1.0",tk.END)
    entities_text.insert(tk.END,entities_json)

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

root.mainloop()