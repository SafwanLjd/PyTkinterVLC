# PyTkinterVLC

This is a simplified version of the [Official VLC Tkinter Example](https://github.com/oaubert/python-vlc/blob/master/examples/tkvlc.py) made to fit my personal needs.

* _Works on Windows [Tested on Windows 10 64-Bit]_
* _Works on Linux (Xorg) [Tested on Arch Linux 64-Bit With DWM]_
* _Probably Won't Work on macOS [Not Tested]


## Usage
### Example
```python
exampleVideoURL = "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_10mb.mp4"
exampleVideoTitle = "Bunny Video"
exampleIconPath = "./icons/vlcCone.ico"
player = Player(video=exampleVideoURL, title=exampleVideoTitle, iconPath=exampleIconPath)
player.start()
```
### Video Player Key Bindings
* Space = Pause/Resume
* Up Arrow = Increase Volume By 5%
* Down Arrow = Decrease Volume By 5%
* Right Arrow = Go Forward 30 seconds
* Left Arrow = Go Backward 30 seconds
* F = Toggle fullscreen
* M = Mute/Unmute
* Q = Quit
* E = Quit