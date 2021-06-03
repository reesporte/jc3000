import numpy as np
from scipy.io.wavfile import write
from .Note import Note, gen_note

class Sequence(object):
    '''create a sequence of notes to play'''

    def __init__(self, fs=44100, fundamental=440, equal=True, voices=1):
        super(Sequence, self).__init__()
        self.fs = fs
        if equal:
            self.init_equal_temperament()
        else:
            self.init_just_temperament()

        self.sequence_notes = []
        self.sequence = []
        self.stacked_notes = None
        for i in range(voices):
            self.sequence.append([])
            self.sequence_notes.append([])

        self.voices = voices
        self.audio = None
        self.fundamental = fundamental

    def init_equal_temperament(self):
        '''set up the basic notes starting with fundamental in equal temperament'''
        notes = {}

        notes['a'] = {'interval': 0 / 12, 'index': 0}
        notes['a#'] = {'interval': 1 / 12, 'index': 1}
        notes['b'] = {'interval': 2 / 12, 'index': 2}
        notes['c'] = {'interval': 3 / 12, 'index': 3}
        notes['c#'] = {'interval': 4 / 12, 'index': 4}
        notes['d'] = {'interval': 5 / 12, 'index': 5}
        notes['d#'] = {'interval': 6 / 12, 'index': 6}
        notes['e'] = {'interval': 7 / 12, 'index': 7}
        notes['f'] = {'interval': 8 / 12, 'index': 8}
        notes['f#'] = {'interval': 9 / 12, 'index': 9}
        notes['g'] = {'interval': 10 / 12, 'index': 10}
        notes['g#'] = {'interval': 11 / 12, 'index': 11}
        self.notes = notes

    def init_just_temperament(self):
        '''set up the basic notes starting with fundamental in just temperament'''
        notes = {}

        notes['uni'] = {'interval': 1, 'index': 0}
        notes['min2'] = {'interval': 25/24, 'index': 1}
        notes['maj2'] = {'interval': 9/8, 'index': 2}
        notes['min3'] = {'interval': 6/5, 'index': 3}
        notes['maj3'] = {'interval': 5/4, 'index': 4}
        notes['4'] = {'interval': 4/3, 'index': 5}
        notes['dim5'] = {'interval': 45/32, 'index': 6}
        notes['5'] = {'interval': 3/2, 'index': 7}
        notes['min6'] = {'interval': 8/5, 'index': 8}
        notes['maj6'] = {'interval': 5/3, 'index': 9}
        notes['min7'] = {'interval': 9/5, 'index': 10}
        notes['maj7'] = {'interval': 15/8, 'index': 11}
        self.notes = notes

    def add_note(self, note, duration=0.25, octave=0, voice=0):
        '''
        adds a note of a given duration (in seconds) and
        octave (relative to note 4) to the sequence at the voice index
        '''
        self.sequence_notes[voice].append(Note(note, duration, octave))
        self.sequence[voice].append(gen_note(duration, octave,
                                      self.notes[note]['interval'], self.fundamental,
                                      self.fs))

    def transpose(self, half_steps=1, voice=0):
        '''regenerate sequence relative to transposed fundamental'''
        self.sequence[voice] = []
        self.fundamental = self.fundamental*2**(half_steps/12)
        for note in self.sequence_notes[voice]:
            self.sequence[voice].append(
                gen_note(
                    note.duration, note.octave,
                    self.notes[note.note],
                    self.fundamental,
                    self.fs
                ))

    def _get_note_key_by_index(self, index: int):
        '''convenience function'''
        for k, v in self.notes.items():
            if v['index'] == index:
                return k

    def _get_note_by_interval(self, note_name: str, interval: int):
        return self._get_note_key_by_index((self.notes[note_name]['index'] + interval) % 12)

    def get_minor_third(self, note_name):
        return self._get_note_by_interval(note_name, 3)

    def get_major_third(self, note_name):
        return self._get_note_by_interval(note_name, 4)

    def get_fifth(self, note_name):
        return self._get_note_by_interval(note_name, 7)

    def get_chromatic_notes(self):
        '''get the names of all the notes'''
        return list(self.notes.keys())

    def get_stacked_notes(self):
        '''concatenate notes'''
        if not self.stacked_notes:
            notes = []
            for s in self.sequence:
                notes.append(np.hstack(s))
            self.stacked_notes = np.column_stack(notes)

        return self.stacked_notes

    def write_file(self, filename):
        '''write audio to wavefile'''
        if filename[-4:] != '.wav':
            filename += '.wav'
        write(filename, self.fs, self.get_stacked_notes())
