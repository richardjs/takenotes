import argparse
import os


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--midi-input', default='Uno',
                        help='regex for selecting MIDI input')
    parser.add_argument('-o', '--midi-output', default='Uno',
                        help='regex for selecting MIDI output')

    parser.add_argument('-d', '--dir', default=os.getcwd(),
                        help='directory in which to save MIDI files')
    parser.add_argument('-f', '--filename-pattern', default='%Y-%m-%d_%H-%M-%S.mid',
                        help='file name patter passed to strftime')

    parser.add_argument('-t', '--new-song-time', type=int, default=10,
                        help='seconds of inactivity to wait before starting a new song')

    return parser.parse_args()
