from datetime import timedelta
from sys import platform
from tkinter import ttk
import tkinter
import vlc

class Player:
    def __init__(self, video, title=None, iconPath=None):
        self.vlcInstance = vlc.MediaPlayer()
        self.vlcInstance.set_mrl(video)

        self.title = title or video
        self.iconPath = iconPath

        self.videoLength = 0
        self.fullScreenState = False
        self.muteState = False
        
        self.__setGUI()
        self.__setBindings()
        self.__onTick()

    def __setGUI(self):
        self.parent = tkinter.Tk()
        self.parent.title(self.title)
        self.parent.iconbitmap(self.iconPath)
        self.parent.minsize(width=800, height=450)
        self.parent.protocol("WM_DELETE_WINDOW", self.exit)

        self.videopanel = ttk.Frame(self.parent)
        self.canvas = tkinter.Canvas(self.videopanel)

        self.canvas.pack(fill=tkinter.BOTH, expand=1)
        self.videopanel.pack(fill=tkinter.BOTH, expand=1)

        self.vlcInstance.set_hwnd(self.videopanel.winfo_id())
        
        self.parent.update()

    def __setBindings(self):
        self.parent.bind("<space>", lambda event: self.pause())
        self.parent.bind("<Right>", lambda event: self.skip(30_000))
        self.parent.bind("<Left>", lambda event: self.skip(-30_000))
        self.parent.bind("<Up>", lambda event: self.setVolume(5))
        self.parent.bind("<Down>", lambda event: self.setVolume(-5))
        self.parent.bind("f", lambda event: self.toggleFullScreen())
        self.parent.bind("m", lambda event: self.toggleMute())
        self.parent.bind("q", lambda event: self.exit())
        self.parent.bind("e", lambda event: self.exit())

    def __onTick(self):
        seconds = self.vlcInstance.get_time() // 1000
        
        if self.videoLength == 0:
            newLength = self.vlcInstance.get_length() // 1000
            if newLength > 0:
                self.videoLength = newLength

        if seconds < 0 or seconds > (2 ** 32):
            seconds = 0
        elif seconds > self.videoLength:
            seconds = self.videoLength

        self.parent.title('[' + str(timedelta(seconds=seconds)) + '/' + str(timedelta(seconds=self.videoLength)) + '] ' + self.title)
        self.parent.after(500, self.__onTick)

    def start(self):
        self.vlcInstance.audio_set_volume(100)
        self.vlcInstance.play()
        self.parent.mainloop()

    def pause(self):
        self.vlcInstance.pause()

    def skip(self, value):
        self.vlcInstance.set_time(self.vlcInstance.get_time() + value)

    def setVolume(self, value):
        self.vlcInstance.audio_set_volume(self.vlcInstance.audio_get_volume() + value)
    
    def toggleFullScreen(self):
        self.fullScreenState = not self.fullScreenState
        self.parent.attributes("-fullscreen", self.fullScreenState)

    def toggleMute(self):
        self.muteState = not self.muteState
        self.vlcInstance.audio_set_mute(self.muteState)

    def exit(self):
        self.vlcInstance.stop()
        self.parent.quit()
        self.parent.destroy()