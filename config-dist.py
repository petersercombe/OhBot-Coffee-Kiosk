##########################
#  Speech Configuration  #
##########################

# After adding your Azure credentials below, rename this file as 'config.py'

# Import speech SDK libraries
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech.audio import AudioOutputConfig

# Configure Azure Cognitive Services Keys
cogKey = '[Insert Azure Key Here]'
cogEndpoint = '[url for your cog services endpoint]'
cogRegion = '[Name of cognitive region, e.g. australiaeast]'

# Configure speech SDK
speech_config = speechsdk.SpeechConfig(subscription=cogKey, region=cogRegion)
audio_config = AudioOutputConfig(use_default_speaker=True)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, language="en-AU")

# Function: listen to microphone input
def fromMic():
    result = speech_recognizer.recognize_once_async().get()
    return result.text


##########################
#    GUI Configuration   #
##########################

# Import GUI libraries
from tkinter import ttk
import tkinter as tk

# GUI Callback function
def varUpdateCallback(var, indx, mode):
    pass

# Set up GUI window
win = tk.Tk()
win.geometry("600x600")
win.wm_title("Robotic Coffee")

# Create Traced Variables
orderText = tk.StringVar()
orderText.set("")
orderText.trace_add('write', varUpdateCallback)

menuText = tk.StringVar()
menuText.set("Coral, the Covid-Safe Kiosk")
menuText.trace_add('write', varUpdateCallback)

# Configure window grid layout
win.rowconfigure(0, weight=1)
win.rowconfigure(1, weight=1)
win.columnconfigure(0, weight=1)

# Create GUI labels
font = ("Gulim", 25)

menuLabel = tk.Label(win, textvariable=menuText, font=font, justify='left')
menuLabel.configure(text=menuText.get())
menuLabel.grid(row=0, column=0, sticky='nw', padx=5, pady=5)

ttk.Separator(win, orient='horizontal').grid(column=0, row=0, sticky='sew')

orderFrame = tk.Frame(win, background='white')
orderLabel = tk.Label(orderFrame, textvariable=orderText, font=font, justify='left', background='white')
orderLabel.configure(text=orderText.get())
orderFrame.grid(row=1, column=0, sticky='nsew')
orderLabel.grid(row=0, column=0, sticky='nw', padx=5, pady=5)

