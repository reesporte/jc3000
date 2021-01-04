# jc3000
A small set of extensible python modules for generating music. Inspired by [this](https://walkerart.org/collections/artworks/wind-chime-after-dream) which was inspired by [this](https://en.wikipedia.org/wiki/John_Cage) (hence the jc3000).

You can generate any notes you want based on any fundamental, and using either just or equal temperament. Shoutout to [this page](https://pages.mtu.edu/~suits/Physicsofmusic.html) for really good instruction on how music and scales work at the physical level. Without this page, I really wouldn't have been able to make this. 

I use [simpleaudio](simpleaudio.readthedocs.io/) to actually play the audio, though in the future I'd like to try using native Python or maybe Cython to do audio playback. I also use [scipy](https://www.scipy.org/) to save the audio as wavfiles, but again, I'd like to see if I could make this a native Python action in the future. I also generate sinwaves with [numpy](https://numpy.org/).

## Examples

* Play the licc
```
from Scales import get_the_licc

the_licc = get_the_licc()

the_licc.play_audio()
the_licc.write_file('the_licc.wav')
```

* Play the C major scale with concert A set to 432 Hz.
```
from Sequence import Sequence

s = Sequence(fundamental=432)

notes = ['c','d','e','f','g','a','b','c']

for i, note in enumerate(notes):
    if i < 5:
        s.add_note(note)
    else:
        s.add_note(note, octave=1)
        
s.play_audio()
```

## Note
This is really bare bones and simple, but it's quite effective I think. You can really do anything you want with it. I'm thinking about adding in attack and release features at some point, but I have to learn more about how they work IRL to know how to represent that in a computer. 
