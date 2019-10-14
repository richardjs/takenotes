import datetime
import os
import re
import sys
import time

import mido


import takenotes.cli


TICKS_PER_BEAT = 480


def save_song(msgs):
    mid = mido.MidiFile()
    mid.ticks_per_beat = TICKS_PER_BEAT

    last_time = msgs[0].time
    for msg in msgs:
        ticks = int(mido.second2tick(
            msg.time - last_time, TICKS_PER_BEAT, 500000))
        last_time = msg.time
        msg.time = ticks
    track = mido.MidiTrack(msgs)

    mid.tracks.append(track)
    mid.save(datetime.datetime.now().strftime(
        os.path.join(args.dir, args.filename_pattern)))


args = takenotes.cli.cli()


print('Looking for input %s...' % args.midi_input)
input_name = None
for name in mido.get_input_names():
    if re.search(args.midi_input, name):
        input_name = name
        print('Found input %s' % input_name)
        break
if not input_name:
    print('ERROR: Could not find %s amoung inputs {%s}!' % (
        args.midi_input,
        ', '.join(mido.get_input_names())
    ))
    sys.exit(1)
inport = mido.open_input(input_name)


print('Looking for output %s...' % args.midi_output)
output_name = None
for name in mido.get_output_names():
    if re.search(args.midi_output, name):
        output_name = name
        print('Found output %s' % output_name)
        break
if not output_name:
    print('WARNING: Could not find %s amoung outputs {%s}!' % (
        args.midi_output,
        ', '.join(mido.get_output_names())
    ))
outport = mido.open_output(output_name)


last_msg_time = time.time()
msgs = []
while 1:
    if msgs and time.time() - last_msg_time > args.new_song_time:
        save_song(msgs)
        outport.send(mido.Message('note_on', note=96))
        outport.send(mido.Message('note_on', note=103))
        msgs = []

    for msg in inport.iter_pending():
        if msg.type == 'clock':
            continue
        print(msg)
        msg.time = time.time()
        msgs.append(msg)
        last_msg_time = time.time()
