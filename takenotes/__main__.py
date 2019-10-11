import re
import sys
import time

import mido

INPUT_NAME = r'Uno'
OUTPUT_NAME = r'Uno'
SONG_FILE_PATTERN = '/tmp/%Y-%m-%d_%H-%M-%S.mid'
NEW_SONG_TIME = 10

TICKS_PER_BEAT = 480


print('Looking for input %s...' % INPUT_NAME)
input_name = None
for name in mido.get_input_names():
    if re.search(INPUT_NAME, name):
        input_name = name
        print('Found input %s' % input_name)
        break
if not input_name:
    print('ERROR: Could not find %s amoung inputs {%s}!' % (
        INPUT_NAME,
        ', '.join(mido.get_input_names())
    ))
    sys.exit(1)
inport = mido.open_input(input_name)


print('Looking for output %s...' % OUTPUT_NAME)
output_name = None
for name in mido.get_output_names():
    if re.search(OUTPUT_NAME, name):
        output_name = name
        print('Found output %s' % output_name)
        break
if not output_name:
    print('WARNING: Could not find %s amoung outputs {%s}!' % (
        OUTPUT_NAME,
        ', '.join(mido.get_output_names())
    ))
outport = mido.open_output(output_name)


last_msg_time = time.time()
msgs = []
while 1:
    if msgs and time.time() - last_msg_time > NEW_SONG_TIME:
        mid = mido.MidiFile()
        mid.ticks_per_beat = TICKS_PER_BEAT

        last_time = msgs[0].time
        for msg in msgs:
            ticks = int(mido.second2tick(msg.time - last_time, TICKS_PER_BEAT, 500000))
            last_time = msg.time
            msg.time = ticks
        track = mido.MidiTrack(msgs)

        mid.tracks.append(track)
        mid.save(datetime.datetime.now().strftime(SONG_FILE_PATTERN))

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
