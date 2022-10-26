from tkinter import *
from tkinter.ttk import *
from tk_tools import *
from threading import Thread
from pygame import mixer, error
from tkinter import messagebox
from pynput.keyboard import Listener
import keyboard
def degis():
    if chk.instate(['selected']):
        label1.config(foreground=('#00ff00'), text='OK-This location is\naccepting trick-or-treaters.')
        label2.set_value(str(ctrlScreen.totc.get()))
        label3.set_value(str(ctrlScreen.candyTaken.get()))
        label4.set_value(candyLeft.get())
        playButton.config(state=NORMAL)
        prevButton.config(state=NORMAL)
        nextButton.config(state=NORMAL)
    else:
        label1.config(foreground=('#ff0000'), text='DND-This location is not\naccepting trick-or-treaters.')
        label2.set_value('')
        label3.set_value('')
        label4.set_value('')
        stop()
        playButton.config(state=DISABLED)
        prevButton.config(state=DISABLED)
        nextButton.config(state=DISABLED)
        root.track=1
def setUnknown():
    candyLeft.set('')
    degis()
def close():
    stop()
    ctrlScreen.destroy()
    displayScreen.destroy()
def previous():
    if root.track>1:
        root.track-=1
    root.paused=False
    stop()
    play()
def next_track():
    if 7>root.track:
        root.track+=1
    root.paused=False
    stop()
    play()
def detect():
    if root.playing and not mixer.music.get_busy() and not root.paused and not root.stopped:
        if 7>root.track:
            next_track()
        elif root.stopped:
            return
        else:
            root.track=1
            stop()
            play()
    root.after(10, detect)
def play():
    try:
        if root.paused:
            mixer.music.unpause()
            root.paused=False
        else:
            mixer.music.load('track_'+str(root.track)+'.mp3')
            if loopButton.instate(['selected']):
                mixer.music.play(-1)
            else:
                mixer.music.play()
            detect()
            loopButton.config(state=DISABLED)
        statusLabel.config(text='Track '+str(root.track))
        playButton.config(text='||')
        loopButton.state(['!alternate'])
        root.playing=True
        root.stopped=False
    except error as e:
        statusLabel.config(text='Error')
        messagebox.showerror('Error', str(e))
def pause():
    if root.playing:
        root.playing=False
        root.paused=True
        mixer.music.pause()
        statusLabel.config(text=' Pause ')
        playButton.config(text='|>')
def stop():
    root.stopped=True
    mixer.music.stop()
    root.playing=False
    statusLabel.config(text='  Stop  ')
    playButton.config(text='|>')
    loopButton.config(state=NORMAL)
    loopButton.state(['!alternate'])
def change_volume(v):
    mixer.music.set_volume(int(float(v))/100)
def play_pause():
    if root.playing:
        pause()
    else:
        play()
def myfunc(v):
    if not candyLeft.get()=='':
        if int(candyLeft.get())>0:
            candyLeft.set(str(int(candyLeft.get())-1))
            if int(candyLeft.get())==0:
                chk.state(['!selected'])
                degis()
def listener():
    if keyboard.is_pressed('f12'):
        if keyboard.is_pressed('shift'):
            if ctrlScreen.candyTaken.get()<9999:
                ctrlScreen.candyTaken.set(ctrlScreen.candyTaken.get()+1)
                myfunc(None)
        elif keyboard.is_pressed('ctrl'):
            if ctrlScreen.totc.get()<999:
               ctrlScreen.totc.set(ctrlScreen.totc.get()+1)
        degis()
        while keyboard.is_pressed('f12'):
            pass
    elif keyboard.is_pressed('f11'):
        if keyboard.is_pressed('shift'):
            if ctrlScreen.candyTaken.get()>0:
                ctrlScreen.candyTaken.set(ctrlScreen.candyTaken.get()-1)
        elif keyboard.is_pressed('ctrl'):
            if ctrlScreen.totc.get()>0:
               ctrlScreen.totc.set(ctrlScreen.totc.get()-1)
        degis()
        while keyboard.is_pressed('f11'):
            pass
    ctrlScreen.after(10, listener)
ctrlScreen=Tk()
ctrlScreen.title('Control Screen-Halloween Center v1.0')
ctrlScreen.resizable(False, False)
ctrlScreen.grid()
ctrlScreen.totc=IntVar()
ctrlScreen.candyTaken=IntVar()
frame1=LabelFrame(text='Display Controls')
frame1.grid(column=1, row=1)
candyLeft=StringVar()
chk=Checkbutton(frame1, text='Accept trick-or-treaters', command=degis)
chk.pack()
chk.state(['!alternate'])
chk.state(['selected'])
mixer.init()
Label(frame1, text='Trick-or-Treater Counter').pack()
Spinbox(frame1, textvariable=ctrlScreen.totc, from_=0, to=999, state='readonly', command=degis).pack()
Label(frame1, text='Candies Taken').pack()
sb=Spinbox(frame1, textvariable=ctrlScreen.candyTaken, from_=0, to=9999, state='readonly', command=degis)
sb.pack()
sb.bind('<<Increment>>', myfunc)
Label(frame1, text='Candies Left').pack()
Spinbox(frame1, textvariable=candyLeft, from_=0, to=9999, state='readonly', command=degis).pack()
Button(frame1, text='Unknown', command=setUnknown).pack()
root=LabelFrame(text='Music Controls')
root.grid(column=2, row=1)
root.grid()
root.playing=False
root.stopped=True
root.paused=False
ctrlScreen.iconbitmap('pumpkin.ico')
root.track=1
statusLabel=Label(root, text='  Stop  ')
statusLabel.grid(column=5, row=3)
prevButton=Button(root, text='|<<', command=previous)
prevButton.grid(column=1, row=3)
playButton=Button(root, text='|>', command=play_pause)
playButton.grid(column=2, row=3)
Button(root, text='×', command=stop).grid(column=3, row=3)
nextButton=Button(root, text='>>|', command=next_track)
nextButton.grid(column=4, row=3)
volumeSlider=Scale(root, from_=0, to=100, command=change_volume)
volumeSlider.grid(column=4, row=4)
volumeSlider.set(100)
Label(root, text='Volume').grid(column=3, row=4)
loopButton=Checkbutton(root, text='Loop')
loopButton.grid(column=1, row=4)
menu=Menu(root)
loopButton.state(['!alternate'])
displayScreen=Tk()
displayScreen.title('Display Screen-Halloween Center v1.0')
displayScreen.config(background='black')
displayScreen.resizable(False, False)
displayScreen.iconbitmap('pumpkin.ico')
label1=Label(displayScreen, background='black', foreground='#00ff00', text='OK-This location is\naccepting trick-or-treaters.', font=('5by7', 50))
label1.pack()
Label(displayScreen, text='Trick-or-Treater Counter', font=('Segoe UI', 25), background='black', foreground='white').pack()
label2=SevenSegmentDigits(displayScreen, digits=3, background='black', digit_color='yellow', height=100)
label2.pack()
Label(displayScreen, text='Candies Taken', font=('Segoe UI', 25), background='black', foreground='white').pack()
label3=SevenSegmentDigits(displayScreen, digits=4, background='black', digit_color='yellow', height=100)
label3.pack()
Label(displayScreen, text='Candies Left (if blank, unknown)', font=('Segoe UI', 25), background='black', foreground='white').pack()
label4=SevenSegmentDigits(displayScreen, digits=4, background='black', digit_color='yellow', height=100)
label4.pack()
ctrlScreen.protocol('WM_DELETE_WINDOW', close)
displayScreen.protocol('WM_DELETE_WINDOW', close)
degis()
listener()
displayScreen.mainloop()



