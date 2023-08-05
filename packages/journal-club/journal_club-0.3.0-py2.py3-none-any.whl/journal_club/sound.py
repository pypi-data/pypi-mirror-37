import time
import os
import pyglet
from gtts import gTTS
from pydub import AudioSegment
import traceback

def play_text(*txts):
    try:
        sounds = []
        fnames = []
        for i, s in enumerate(txts):
            g = gTTS(text=s, lang='en')
            fname = 'voice{}.mp3'.format(i)
            with open(fname, 'wb') as file:
                g.write_to_fp(file)
            mp3 = AudioSegment.from_mp3(fname)
            fname = fname.replace('.mp3', '.wav')
            mp3.export(fname, format='wav')
            os.remove(fname.replace('.wav', '.mp3'))
            sounds.append(pyglet.media.load(fname, streaming=False))
            fnames.append(fname)
        s = time.time()
        duration = max(sound.duration for sound in sounds)
        for sound in sounds:
            sound.play()
        while time.time() < s + duration + 0.1:
            time.sleep(0.1)
        for fname in fnames:
            os.remove(fname)
    except Exception as e:
        print("Warning: playback failed with the following error\n=====")
        traceback.print_exc()
        print("\n=====")

def play_sound(fname, start=0, duration=None, block=False):
    try:
        sound = pyglet.media.load(fname, streaming=False)
        if duration is None:
            duration = sound.duration
        s = time.time()
        p = sound.play()
        p.seek(start)
        if block:
            while time.time() < s + duration + 0.1 - start:
                time.sleep(0.1)
            p.pause()
    except:
        print("Warning: playback failed")


if __name__ == '__main__':
    from journal_club import where_jc
    play_sound(os.path.join(where_jc, 'countdown.wav'))
    play_text('hello')
