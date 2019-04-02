import npyscreen
import os
import time
from pynput.keyboard import Key, Controller


class track():
    def __init__(self, length, title, path):
        self.length = length
        self.title = title
        self.path = path


def parsem3u(infile):
    try:
        assert(type(infile) == '_io.TextIOWrapper')
    except AssertionError:
        infile = open(infile, 'r', encoding='utf-8')
    line = infile.readline()
    if not line.startswith('#EXTM3U'):
        return
    playlist = []
    song = track(None, None, None)

    for line in infile:
        line = line.strip()
        if line.startswith('#EXTINF:'):
            length, title = line.split('#EXTINF:')[1].split(',', 1)
            song = track(length, title, None)
        elif len(line) != 0:
            song.path = line
            playlist.append(song)
            song = track(None, None, None)

    infile.close()

    return playlist


def start_vlc(gg):
    cd = "cd %PROGRAMFILES%/VideoLAN/VLC"
    v = "vlc " + gg
    os.system('start')
    time.sleep(1)
    keyboard = Controller()
    keyboard.type(cd)
    keyboard.press(Key.enter)
    keyboard.type(v)
    keyboard.press(Key.enter)
    keyboard.type("exit")
    keyboard.press(Key.enter)
    quit()


class TestApp(npyscreen.NPSApp):
    def main(self):
        m3ufile = 'playlist.m3u'
        playlist = parsem3u(m3ufile)
        options = []
        f = npyscreen.Form(name="IPTV channel search",)
        t = f.add(npyscreen.TitleText, name="Search: ",)
        f.edit()
        f.erase()
        play = []
        for track in playlist:
            if str(t.value).upper() in str(track.title).upper():
                options.append(str(track.title).upper())
                play.append(str(track.path))
        f = npyscreen.Form(name="IPTV channel search", )
        ms = f.add(npyscreen.TitleSelectOne, value=[1, ], name="Please choose channel: ",
                   values=options, scroll_exit=True)
        f.edit()
        gg = play[int(ms.value[0])]
        start_vlc(gg)


if __name__ == "__main__":
    App = TestApp()
    App.run()
    App.main()
