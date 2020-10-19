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
    # Branch that ends current song and starts a new song
    # Must have a song started, no notes_on, and specified time since last message
    if song_started and len(notes_on) == 0 and time.time() - last_msg_time > args.new_song_time:
        filename = datetime.datetime.now().strftime(
            os.path.join(args.dir, args.filename_pattern))
        print(f'Saving {filename}...')
        takenotes.file.save_song(msgs, filename)

        # Notification message
        # TODO: Configuration options?
        outport.send(mido.Message('note_on', note=96))
        outport.send(mido.Message('note_on', note=103))

        # Reset song state
        song_started = False
        msgs = []

    # Process messages
    for msg in inport.iter_pending():
        # We don't care about clock messages
        if msg.type == 'clock':
            continue

        # Start songs on note_on, and keep track of which notes are on
        if msg.type == 'note_on':
            song_started = True
            notes_on.add(msg.note)

        # Remove tracked notes on note_off or note_on with velocity 0
        if msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            notes_on.remove(msg.note)

        t = time.time()
        msg.time = t
        last_msg_time = time.time()
        msgs.append(msg)

        print(msg)
        print(notes_on)
        print(len(msgs))
