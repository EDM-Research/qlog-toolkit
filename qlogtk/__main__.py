#!/bin/python3
from qlogtk.input import read_events, format_event
from qlogtk.output import OutputType, prepare_output, output_data
from qlogtk.action import instantaneous_throughput, test, bitrate_ladder
import argparse

action_to_callback_map = {
    "calculate_instantaneous_throughput": {
        'process': instantaneous_throughput.calculate,
        'output': instantaneous_throughput.output,
    },
    "bitrate_ladder": {
        'process': bitrate_ladder.calculate,
        'output': bitrate_ladder.output,
    },
    "test": {
        'process': test.calculate,
        'output': test.output,
    }
}


def execute_actions(actions, inputs, output):
    outputs = prepare_output(output, inputs, actions)

    for a_i in range(len(actions)):
        action = action_to_callback_map.get(actions[a_i])

        if not action:
            raise Exception('could not execute action:', actions[a_i])
        else:
            # execute action on inputs
            for i_i in range(len(inputs)):
                for event in read_events(inputs[i_i]):
                    event = format_event(event)
                    outputs[a_i][i_i] = action['process'](event, outputs[a_i][i_i])

                outputs[a_i][i_i] = action['output'](output, outputs[a_i][i_i])

    output_data(output, outputs)


def main():
    action_choices = []
    for k in action_to_callback_map:
        action_choices.append(k)

    argument_parser = argparse.ArgumentParser(
        prog="qlog-toolkit", description="qlog toolkit")

    argument_parser.add_argument(
        "-a", "--actions", required=True, nargs='+', choices=action_choices)
    argument_parser.add_argument("-o", "--output", required=True,
                                 choices=[OutputType.JSON, OutputType.Matplotlib])
    argument_parser.add_argument('inputs', nargs='+')

    arguments = argument_parser.parse_args()

    execute_actions(arguments.actions, arguments.inputs, arguments.output)


if __name__ == "__main__":
    main()
