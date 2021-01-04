import numpy as np
from scipy.io.wavfile import write
import simpleaudio as sa
from Note import Note, gen_note

class Sequence(object):
    """create a sequence of notes to play"""
    # i mean sequence in the mathematical sense, not musical, but
    # you could technically use this class to make a sequence in the musical sense
    # but you don't have to, which is the main point i'm trying to make
    def __init__(self, fs=44100, fundamental=440, equal=True):
        # default sampling rate is 44100 because
        # [https://en.wikipedia.org/wiki/44,100_Hz#Origin]
        # default concert a is 440 hz bc
        # [https://en.wikipedia.org/wiki/A440_(pitch_standard)]
        super(Sequence, self).__init__()
        self.fs = fs
        if equal:
            self.notes = self.init_equal_temperament()
        else:
            self.notes = self.init_just_temperament()
        self.sequence_notes = []
        self.sequence = []
        self.frequencies = []
        self.audio = None
        self.duration = 0
        self.fundamental = fundamental
        self.equal = equal

    def init_equal_temperament(self):
        """set up the basic notes starting with fundamental"""
        notes = {}

        notes['a'] = 0 / 12
        notes['a#'] = 1 / 12
        notes['b'] = 2 / 12
        notes['c'] = 3 / 12
        notes['c#'] = 4 / 12
        notes['d'] = 5 / 12
        notes['d#'] = 6 / 12
        notes['e'] = 7 / 12
        notes['f'] = 8 / 12
        notes['f#'] = 9 / 12
        notes['g'] = 10 / 12
        notes['g#'] = 11 / 12
        return notes

    def init_just_temperament(self):
        """set up the basic notes starting with fundamental"""
        notes = {}

        notes['uni'] = 1
        notes['min2'] = 25/24
        notes['maj2'] = 9/8
        notes['min3'] = 6/5
        notes['maj3'] = 5/4
        notes['4'] = 4/3
        notes['dim5'] = 45/32
        notes['5'] = 3/2
        notes['min6'] = 8/5
        notes['maj6'] = 5/3
        notes['min7'] = 9/5
        notes['maj7'] = 15/8
        return notes

    def add_note(self,note,duration=0.25,octave=0):
        """
        adds a note of a given duration (in seconds) and
        octave (relative to note_4) to the sequence
        """
        self.duration += duration
        self.sequence_notes.append(Note(note, duration, octave))
        self.sequence.append(gen_note(duration, octave,
                                      self.notes[note], self.fundamental,
                                      self.fs))
        self.frequencies.append(self.fundamental * (self.notes[note]) * (2**octave))

    def transpose(self, half_steps=1):
        """regenerate sequence relative to transposed fundamental"""
        self.sequence = []
        self.fundamental = self.fundamental*2**(half_steps/12)
        for note in self.sequence_notes:
            self.sequence.append(
                             gen_note(
                                note.duration, note.octave,
                                self.notes[note.note],
                                self.fundamental,
                                self.fs
                                ))
                                
    def get_chromatic_notes(self):
        """get the names of all the notes"""
        return list(self.notes.keys())

    def write_file(self, filename):
        """write audio to wavefile"""
        # concatenate notes
        audio = np.hstack(self.sequence)
        # write to file
        write(filename, self.fs, audio)

    def play_audio(self):
        """play sequence of notes"""
        # concatenate notes
        audio = np.hstack(self.sequence)
        # Start playback
        play_obj = sa.play_buffer(audio_data=audio, num_channels=1,
                                  bytes_per_sample=2, sample_rate=self.fs)
        # Wait for playback to finish before exiting
        play_obj.wait_done()
