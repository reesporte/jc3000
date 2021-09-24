import struct
import sys
import numpy as np
from .Note import Note, gen_note


class Sequence(object):
    """create a sequence of notes to play"""

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
        """set up the basic notes starting with fundamental in equal temperament"""
        notes = {}

        notes["a"] = {"interval": 0 / 12, "index": 0}
        notes["a#"] = {"interval": 1 / 12, "index": 1}
        notes["b"] = {"interval": 2 / 12, "index": 2}
        notes["c"] = {"interval": 3 / 12, "index": 3}
        notes["c#"] = {"interval": 4 / 12, "index": 4}
        notes["d"] = {"interval": 5 / 12, "index": 5}
        notes["d#"] = {"interval": 6 / 12, "index": 6}
        notes["e"] = {"interval": 7 / 12, "index": 7}
        notes["f"] = {"interval": 8 / 12, "index": 8}
        notes["f#"] = {"interval": 9 / 12, "index": 9}
        notes["g"] = {"interval": 10 / 12, "index": 10}
        notes["g#"] = {"interval": 11 / 12, "index": 11}
        self.notes = notes

    def init_just_temperament(self):
        """set up the basic notes starting with fundamental in just temperament"""
        notes = {}

        notes["a"] = {"interval": 1, "index": 0}
        notes["a#"] = {"interval": 25 / 24, "index": 1}
        notes["b"] = {"interval": 9 / 8, "index": 2}
        notes["c"] = {"interval": 6 / 5, "index": 3}
        notes["c#"] = {"interval": 5 / 4, "index": 4}
        notes["d"] = {"interval": 4 / 3, "index": 5}
        notes["d#"] = {"interval": 45 / 32, "index": 6}
        notes["e"] = {"interval": 3 / 2, "index": 7}
        notes["f"] = {"interval": 8 / 5, "index": 8}
        notes["f#"] = {"interval": 5 / 3, "index": 9}
        notes["g"] = {"interval": 9 / 5, "index": 10}
        notes["g#"] = {"interval": 15 / 8, "index": 11}
        self.notes = notes

    def add_note(self, note, duration=0.25, octave=0, voice=0, silent=False):
        """
        adds a note of a given duration (in seconds) and
        octave (relative to note 4) to the sequence at the voice index
        """
        self.sequence_notes[voice].append(Note(note, duration, octave))
        self.sequence[voice].append(
            gen_note(
                duration, octave, self.notes[note]["interval"], self.fundamental, self.fs, silent
            )
        )

    def transpose(self, half_steps=1, voice=0):
        """regenerate sequence relative to transposed fundamental"""
        self.sequence[voice] = []
        self.fundamental = self.fundamental * 2 ** (half_steps / 12)
        for note in self.sequence_notes[voice]:
            self.sequence[voice].append(
                gen_note(
                    note.duration, note.octave, self.notes[note.note], self.fundamental, self.fs
                )
            )

    def _get_note_key_by_index(self, index: int):
        """convenience function"""
        for k, v in self.notes.items():
            if v["index"] == index:
                return k

    def _get_note_by_interval(self, note_name: str, interval: int):
        return self._get_note_key_by_index((self.notes[note_name]["index"] + interval) % 12)

    def get_minor_third(self, note_name):
        return self._get_note_by_interval(note_name, 3)

    def get_major_third(self, note_name):
        return self._get_note_by_interval(note_name, 4)

    def get_fifth(self, note_name):
        return self._get_note_by_interval(note_name, 7)

    def get_chromatic_notes(self):
        """get the names of all the notes"""
        return list(self.notes.keys())

    def get_stacked_notes(self):
        """concatenate notes"""
        if not self.stacked_notes:
            notes = []
            for s in self.sequence:
                notes.append(np.hstack(s))
            self.stacked_notes = np.column_stack(notes)

        return self.stacked_notes

    def write_file(self, filename):
        """write audio to wavefile"""
        if filename[-4:] != ".wav":
            filename += ".wav"
        write(filename, self.fs, self.get_stacked_notes())


def write(filename, rate, data):
    """
    lifted from the scipy source[https://github.com/scipy/scipy/blob/v1.7.1/scipy/io/wavfile.py#L710-L834],
    licensed with BSD3 license [https://github.com/scipy/scipy/blob/master/LICENSE.txt]
    """
    if hasattr(filename, "write"):
        fid = filename
    else:
        fid = open(filename, "wb")

    fs = rate

    try:
        dkind = data.dtype.kind
        if not (dkind == "i" or dkind == "f" or (dkind == "u" and data.dtype.itemsize == 1)):
            raise ValueError("Unsupported data type '%s'" % data.dtype)

        header_data = b""

        header_data += b"RIFF"
        header_data += b"\x00\x00\x00\x00"
        header_data += b"WAVE"

        # fmt chunk
        header_data += b"fmt "
        if dkind == "f":
            format_tag = 0x0003
        else:
            format_tag = 0x0001
        if data.ndim == 1:
            channels = 1
        else:
            channels = data.shape[1]
        bit_depth = data.dtype.itemsize * 8
        bytes_per_second = fs * (bit_depth // 8) * channels
        block_align = channels * (bit_depth // 8)

        fmt_chunk_data = struct.pack(
            "<HHIIHH", format_tag, channels, fs, bytes_per_second, block_align, bit_depth
        )
        if not (dkind == "i" or dkind == "u"):
            # add cbSize field for non-PCM files
            fmt_chunk_data += b"\x00\x00"

        header_data += struct.pack("<I", len(fmt_chunk_data))
        header_data += fmt_chunk_data

        # fact chunk (non-PCM files)
        if not (dkind == "i" or dkind == "u"):
            header_data += b"fact"
            header_data += struct.pack("<II", 4, data.shape[0])

        # check data size (needs to be immediately before the data chunk)
        if ((len(header_data) - 4 - 4) + (4 + 4 + data.nbytes)) > 0xFFFFFFFF:
            raise ValueError("Data exceeds wave file size limit")

        fid.write(header_data)

        # data chunk
        fid.write(b"data")
        fid.write(struct.pack("<I", data.nbytes))
        if data.dtype.byteorder == ">" or (data.dtype.byteorder == "=" and sys.byteorder == "big"):
            data = data.byteswap()
        _array_tofile(fid, data)

        # Determine file size and place it in correct
        #  position at start of the file.
        size = fid.tell()
        fid.seek(4)
        fid.write(struct.pack("<I", size - 8))

    finally:
        if not hasattr(filename, "write"):
            fid.close()
        else:
            fid.seek(0)


def _array_tofile(fid, data):
    # ravel gives a c-contiguous buffer
    fid.write(data.ravel().view("b").data)
