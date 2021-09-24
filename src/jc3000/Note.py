import numpy as np


class Note(object):
    """stores information about an individual note in a sequence"""

    def __init__(self, note, duration, octave):
        super(Note, self).__init__()
        self.note = note
        self.duration = duration
        self.octave = octave


def gen_note(duration, octave, interval, concert_a, sample_rate, silent=False):
    """generate notes relative to concert a, duration is in seconds"""

    # TODO: reduce amplitude over time, e.g. implement attack and release
    # like there's a clicking noise in between notes and i think it's because
    # the waves don't match up end to end

    # Generate array with duration*sample_rate steps, ranging between 0 and duration
    t = np.linspace(0, duration, int(duration * sample_rate), False)

    # Generate sine wave relative to concert_a Hz
    if not silent:
        sound = np.sin(concert_a * (2 ** interval) * (2 ** octave) * t * np.pi)
        # Ensure that highest value is in 16-bit range
        audio = sound * (2 ** 15 - 1) / np.max(np.abs(sound))
    else:
        sound = 0 * t
        audio = sound
    # Convert to 16-bit data
    audio = audio.astype(np.int16)

    return audio
