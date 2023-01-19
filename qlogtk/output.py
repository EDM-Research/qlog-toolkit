from enum import Enum
import json
import matplotlib.pyplot as plt


class OutputType(str, Enum):
    JSON = "json"
    Matplotlib = "matplotlib"


def prepare_output(output, input_size, action_size):
    outputs = []

    for _ in range(action_size):
        a_out = []
        for _ in range(input_size):
            a_out.append({})
        outputs.append(a_out)

    if output == OutputType.JSON:
        return outputs
    else:
        raise Exception('output unsupported')


def output_data(output, data):
    if output == OutputType.JSON:
        print(json.dumps(data))
    elif output == OutputType.Matplotlib:
        plt.show()
    else:
        raise Exception('output unsupported')
