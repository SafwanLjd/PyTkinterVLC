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
        self.root = tkinter.Tk()
        self.root.title(self.title)
        self.root.iconbitmap(self.iconPath)
        self.root.minsize(width=800, height=450)
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.videopanel = ttk.Frame(self.root)
        self.canvas = tkinter.Canvas(self.videopanel, bg='#000000', highlightthickness=0)

        self.canvas.pack(fill=tkinter.BOTH, expand=1)
        self.videopanel.pack(fill=tkinter.BOTH, expand=1)

        self.vlcInstance.set_hwnd(self.videopanel.winfo_id())
        
        self.root.update()

    def __setBindings(self):
        self.root.bind("<space>", lambda event: self.vlcInstance.pause())
        self.root.bind("<Right>", lambda event: self.vlcInstance.set_time(self.vlcInstance.get_time() + 30_000))
        self.root.bind("<Left>", lambda event: self.vlcInstance.set_time(self.vlcInstance.get_time() - 30_000))
        self.root.bind("<Up>", lambda event: self.vlcInstance.audio_set_volume(self.vlcInstance.audio_get_volume() + 5))
        self.root.bind("<Down>", lambda event: self.vlcInstance.audio_set_volume(self.vlcInstance.audio_get_volume() - 5))
        self.root.bind("f", lambda event: self.toggleFullScreen())
        self.root.bind("m", lambda event: self.toggleMute())
        self.root.bind("q", lambda event: self.exit())
        self.root.bind("e", lambda event: self.exit())

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

        self.root.title('[' + str(timedelta(seconds=seconds)) + '/' + str(timedelta(seconds=self.videoLength)) + '] ' + self.title)
        self.root.after(500, self.__onTick)

    def start(self):
        self.vlcInstance.audio_set_volume(100)
        self.vlcInstance.play()
        self.root.mainloop()
    
    def toggleFullScreen(self):
        self.fullScreenState = not self.fullScreenState
        self.root.attributes("-fullscreen", self.fullScreenState)

    def toggleMute(self):
        self.muteState = not self.muteState
        self.vlcInstance.audio_set_mute(self.muteState)

    def exit(self):
        self.vlcInstance.stop()
        self.root.quit()
        self.root.destroy()