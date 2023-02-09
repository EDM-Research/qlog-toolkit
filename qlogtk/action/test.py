from qlogtk.output import OutputType


def calculate(event, output):
    if output['data'] == {}:
        output['data']['counter'] = 0
    output['data']['counter'] += 1
    return output


def output(output, data):
    if output == OutputType.Matplotlib:
        if data['ax']._gid == None:
            data['ax'].set_gid(data['action'])
            data['ax'].set_ylabel('events')
        data['ax'].bar(data['input'], data['data']['counter'])

    return data
