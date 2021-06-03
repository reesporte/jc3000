from jc3000 import Sequence
import random

'''generate song in c major with concert A set to 440 hz in equal temperament'''

def main():
    voices = 3
    s = Sequence(fundamental=440, equal=True, voices=voices)
    notes = list('abcdefg')
    time_sig_num = 6
    time_sig_den = 8
    bpm = 60
    song_duration_secs = 180

    last_four_chosen = []
    i = 1

    while song_duration_secs > 0:
        note = random.choice(notes)

        while note in last_four_chosen:
            note = random.choice(notes)
        i += 1

        if i == 4:
            last_four_chosen = []
            i = 0

        duration = ((random.randint(1, time_sig_num) / time_sig_den) * 60) / bpm
        song_duration_secs -= duration

        s.add_note(note, duration, random.randint(-1, 1), voice=0)
        s.add_note(s.get_fifth(note), duration,
                   random.randint(-1, 1), voice=1)
        s.add_note(s.get_major_third(note), duration,
                   random.randint(-1, 1), voice=2)

    s.write_file('c_major_improv.wav')


if __name__ == '__main__':
    main()
