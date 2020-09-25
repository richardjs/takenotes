import datetime
import os
import re
import sys
import time

import mido

import takenotes.cli
import takenotes.file
import takenotes.ports


args = takenotes.cli.cli()


inport, outport = takenotes.ports.open_ports(args.midi_input, args.midi_output)


last_msg_time = time.time()
song_started = False
msgs = []
notes_on = set()
while 1:
    if song_started and len(notes_on) == 0 and time.time() - last_msg_time > args.new_song_time:
        takenotes.file.save_song(msgs, datetime.datetime.now().strftime(
            os.path.join(args.dir, args.filename_pattern)))
        outport.send(mido.Message('note_on', note=96))
        outport.send(mido.Message('note_on', note=103))
        msgs = []
        song_started = False

    for msg in inport.iter_pending():
        if msg.type == 'clock':
            continue
        if msg.type == 'note_on':
            song_started = True
            notes_on.add(msg.note)
        if msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            notes_on.remove(msg.note)
        print(msg)
        print(notes_on)
        msg.time = time.time()
        msgs.append(msg)
        print(len(msgs))
        last_msg_time = time.time()
