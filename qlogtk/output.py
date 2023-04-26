from enum import Enum
import json
import matplotlib.pyplot as plt


class OutputType(str, Enum):
    JSON = "json"
    Matplotlib = "matplotlib"


def prepare_output(output, inputs, actions):
    if output in [OutputType.JSON]:
        return prepare_output_default(output, inputs, actions)
    elif output == OutputType.Matplotlib:
        return prepare_output_matplotlib(inputs, actions)
    else:
        raise Exception('output unsupported')


def prepare_output_matplotlib(inputs, actions):
    outputs = []

    for a_i in range(len(actions)):
        action = actions[a_i]
        a_out = []

        single = False
        fig = None
        axes = None

        # single chart
        if action in ['test']:
            single = True
            fig, ax = plt.subplots(1, 1, sharex=True, sharey=True)
            axes = [ax]*len(inputs)
        else:
            fig, axes = plt.subplots(1, len(inputs), sharex=True, sharey=True)
            if len(inputs) < 2:
                axes = [axes]
        fig.suptitle(action)
        for i_i in range(len(inputs)):
            input = inputs[i_i]
            a_out.append({
                'input': input,
                'output': OutputType.Matplotlib,
                'action': action,
                'data': {},
                'ax': axes[i_i],
            })
            if not single:
                axes[i_i].set_title(input)
        outputs.append(a_out)

    return outputs


def prepare_output_default(output, inputs, actions):
    outputs = []

    for a_i in range(len(actions)):
        action = actions[a_i]
        a_out = []
        for i_i in range(len(inputs)):
            input = inputs[i_i]
            a_out.append({
                'input': input,
                'output': output,
                'action': action,
                'data': {},
            })
        outputs.append(a_out)

    return outputs


def output_data(output, data):
    if output == OutputType.JSON:
        print(json.dumps(data))
    elif output == OutputType.Matplotlib:
        plt.show()
    else:
        raise Exception('output unsupported')
