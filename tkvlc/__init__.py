from datetime import timedelta
from sys import platform
from tkinter import ttk
import tkinter
import vlc
import os

isLinux = platform.startswith('linux')

class Player:
	def __init__(self, video, title=None, iconPath=None, showOutput=False, vlcArgs=[]):
		if isLinux and '--no-xlib' not in vlcArgs:
			vlcArgs.append('--no-xlib')

		self.vlcInstance = vlc.Instance(vlcArgs)
		self.mediaPlayer = self.vlcInstance.media_player_new()
		self.mediaPlayer.set_media(self.vlcInstance.media_new(video))

		self.title = title or video
		self.iconPath = iconPath

		self.videoLength = 0
		self.fullScreenState = False
		self.muteState = False
		
		if not showOutput:
			self.__suppressOutput()
		
		self.__setGUI()
		self.__setBindings()
		self.__onTick()

	def __setGUI(self):
		self.root = tkinter.Tk()
		self.root.title(self.title)
		self.root.iconbitmap(self.iconPath)
		self.root.minsize(width=800, height=450)
		self.root.protocol('WM_DELETE_WINDOW', self.exit)
		self.videoPanel = ttk.Frame(self.root)
		self.canvas = tkinter.Canvas(self.videoPanel, bg='#000000', highlightthickness=0)

		self.canvas.pack(fill=tkinter.BOTH, expand=1)
		self.videoPanel.pack(fill=tkinter.BOTH, expand=1)
		
		winfoID = self.videoPanel.winfo_id()
		
		if isLinux:
			self.mediaPlayer.set_xwindow(winfoID) 
		else:
			self.mediaPlayer.set_hwnd(winfoID)

		self.root.update()

	def __setBindings(self):
		self.root.bind('<space>', lambda event: self.mediaPlayer.pause())
		self.root.bind('<Right>', lambda event: self.mediaPlayer.set_time(self.mediaPlayer.get_time() + 30_000))
		self.root.bind('<Left>', lambda event: self.mediaPlayer.set_time(self.mediaPlayer.get_time() - 30_000))
		self.root.bind('<Up>', lambda event: self.mediaPlayer.audio_set_volume(self.mediaPlayer.audio_get_volume() + 5))
		self.root.bind('<Down>', lambda event: self.mediaPlayer.audio_set_volume(self.mediaPlayer.audio_get_volume() - 5))
		self.root.bind('f', lambda event: self.toggleFullScreen())
		self.root.bind('m', lambda event: self.toggleMute())
		self.root.bind('q', lambda event: self.exit())
		self.root.bind('e', lambda event: self.exit())

	def __onTick(self):
		seconds = self.mediaPlayer.get_time() // 1000

		if self.videoLength == 0:
			newLength = self.mediaPlayer.get_length() // 1000
			
			if newLength > 0:
				self.videoLength = newLength

		if seconds < 0 or seconds > (2 ** 32):
			seconds = 0
		elif seconds > self.videoLength:
			seconds = self.videoLength

		self.root.title('[' + str(timedelta(seconds=seconds)) + '/' + str(timedelta(seconds=self.videoLength)) + '] ' + self.title)
		self.root.after(500, self.__onTick)

	def __suppressOutput(self):
		null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]
		os.dup2(null_fds[0], 1)
		os.dup2(null_fds[1], 2)
		os.close(null_fds[0])
		os.close(null_fds[1])

	def start(self):
		self.mediaPlayer.audio_set_volume(100)
		self.mediaPlayer.play()
		self.root.mainloop()

	def toggleFullScreen(self):
		self.fullScreenState = not self.fullScreenState
		self.root.attributes('-fullscreen', self.fullScreenState)

	def toggleMute(self):
		self.muteState = not self.muteState
		self.mediaPlayer.audio_set_mute(self.muteState)

	def exit(self):
		self.mediaPlayer.stop()
		self.root.quit()
		self.root.destroy()
