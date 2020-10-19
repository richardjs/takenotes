import argparse
import collections

import mido


parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'))
parser.add_argument('-i', '--ignore', action='append', default=[])
args = parser.parse_args()


mid = mido.MidiFile(args.file.name)

message_counts = collections.Counter()
for i, track in enumerate(mid.tracks):
    print('Track {}: {}'.format(i, track.name))

    for msg in track:
        if msg.type in args.ignore:
            continue

        print(msg)
        message_counts[msg.type] += 1

print(f'message counts: {message_counts}')
