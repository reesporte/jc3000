import numpy as np

class Note(object):
    """stores information about an individual note in a sequence"""
    def __init__(self, note, duration, octave):
        super(Note, self).__init__()
        self.note = note
        self.duration = duration
        self.octave = octave

### Utilities ###
def gen_note(duration, octave, note, concert_a, sample_rate):
    """generate notes relative to concert a, duration is in seconds"""
    # Generate array with duration*sample_rate steps, ranging between 0 and duration
    t = np.linspace(0, duration, int(duration * sample_rate), False)
    # Generate sine wave relative to concert_a Hz
    sound = np.sin(concert_a * (2**note) * (2**octave) * t * np.pi)

    # TODO: reduce amplitude over time, e.g. implement attack and release

    # Ensure that highest value is in 16-bit range
    audio = sound * (2**15 - 1) / np.max(np.abs(sound))
    # Convert to 16-bit data
    audio = audio.astype(np.int16)

    return audio
