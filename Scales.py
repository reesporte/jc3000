from Sequence import *

def get_chromatic(EQUAL_TEMPERAMENT):
    if EQUAL_TEMPERAMENT:
        scale = Sequence(fs=44100, fundamental=440, equal=EQUAL_TEMPERAMENT)
        scale.add_note('c')
        scale.add_note('c#')
        scale.add_note('d')
        scale.add_note('d#')
        scale.add_note('e')
        scale.add_note('f')
        scale.add_note('f#')
        scale.add_note('g')
        scale.add_note('g#')
        scale.add_note('a', octave=1)
        scale.add_note('a#', octave=1)
        scale.add_note('b', octave=1)
        scale.add_note('c', octave=1)
    else:
        scale = Sequence(fs=44100, fundamental=261.63, equal=EQUAL_TEMPERAMENT)
        scale.add_note('uni')
        scale.add_note('min2')
        scale.add_note('maj2')
        scale.add_note('min3')
        scale.add_note('maj3')
        scale.add_note('4')
        scale.add_note('dim5')
        scale.add_note('5')
        scale.add_note('min6')
        scale.add_note('maj6')
        scale.add_note('min7')
        scale.add_note('maj7')
        scale.add_note('uni', octave=1)

    return scale

def get_the_licc():
    # the licc
    scale = Sequence(fs=44100, fundamental=440, equal=True)
    scale.add_note('d', duration=.125)
    scale.add_note('e', .125)
    scale.add_note('f', .125)
    scale.add_note('g', .125)
    scale.add_note('e', .257) # .257 for ~swing-iness~
    scale.add_note('c', .125)
    scale.add_note('d', .25)

    scale.play_audio()
