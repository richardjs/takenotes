import mido

def open_ports(midi_input=None, midi_output=None):
    if midi_input:
        print('Looking for input %s...' % midi_input)
        input_name = None
        for name in mido.get_input_names():
            if re.search(midi_input, name):
                input_name = name
                print('Found input %s' % input_name)
                break
        if not input_name:
            print('ERROR: Could not find %s amoung inputs {%s}!' % (
                midi_input,
                ', '.join(mido.get_input_names())
            ))
            sys.exit(1)
        inport = mido.open_input(input_name)
    else:
        print('Opening virtual input')
        inport = mido.open_input('takenotes in', virtual=True)

    if midi_output:
        print('Looking for output %s...' % midi_output)
        output_name = None
        for name in mido.get_output_names():
            if re.search(midi_output, name):
                output_name = name
                print('Found output %s' % output_name)
                break
        if not output_name:
            print('WARNING: Could not find %s amoung outputs {%s}!' % (
                midi_output,
                ', '.join(mido.get_output_names())
            ))
        outport = mido.open_output(output_name)
    else:
        print('Opening virtual output')
        outport = mido.open_output('takenotes out', virtual=True)

    return inport, outport
