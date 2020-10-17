import mido


TICKS_PER_BEAT = 480


def save_song(msgs, filename):
    mid = mido.MidiFile()
    mid.ticks_per_beat = TICKS_PER_BEAT

    first_time = None
    for msg in msgs:
        if msg.type == 'note_on':
            first_time = msg.time
            break

    last_time = first_time
    for msg in msgs:
        if msg.time < first_time:
            t = 0
        else:
            t = msg.time - last_time
        ticks = int(mido.second2tick(t, TICKS_PER_BEAT, 500000))
        last_time = msg.time
        msg.time = ticks
    track = mido.MidiTrack(msgs)

    mid.tracks.append(track)
    mid.save(filename)
