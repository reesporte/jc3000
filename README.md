# jc3000
A small python package for generating music. Inspired by [this](https://walkerart.org/collections/artworks/wind-chime-after-dream) which was inspired by [this](https://en.wikipedia.org/wiki/John_Cage) (that's why it's called jc3000).

You can generate any notes you want based on any [fundamental](https://en.wikipedia.org/wiki/Fundamental_frequency) _(the frequency of concert A in this case, fundamental as a term is used kind of loosely)_. You can also use either just or equal [temperament](https://pages.mtu.edu/~suits/scales.html). 

## More reading
[This page](https://pages.mtu.edu/~suits/Physicsofmusic.html) has really good information on how music and scales work at the physical level. 

Default sample rate is [44,100 Hz](https://en.wikipedia.org/wiki/44,100_Hz#Origin).  
Default concert A is [440 Hz](https://en.wikipedia.org/wiki/A440_(pitch_standard)).  

## Installation
You can install it via pip. It requires numpy. Probably not compatible with python <= 3.6.  

```
python3 -m pip install jc3000
```

## Examples

* Play the licc
```
from jc3000 import Sequence

s = Sequence(fs=44100, fundamental=440, equal=True)
s.add_note('d', duration=.125)
s.add_note('e', .125)
s.add_note('f', .125)
s.add_note('g', .125)
s.add_note('e', .257)  # .257 for ~swing-iness~
s.add_note('c', .125)
s.add_note('d', .25)

s.write_file('the_licc.wav')
```

* Play the C major scale with concert A set to 432 Hz.
```
from jc3000 import Sequence

s = Sequence(fundamental=432)

notes = ['cdefgabc']

for i, note in enumerate(notes):
    if i < 5:
        s.add_note(note)
    else:
        s.add_note(note, octave=1)
        
s.write_file('cmajor_432hz.wav')
```
