from qlogtk.output import OutputType


def calculate(event, output):
    if output['data'] == {}:
        output['data']['bitrate'] = []

    if event['category'] == 'abr' \
            and event['type'] == 'representation_switch' \
            and event['data']['media_type'] == 'video':
        
        output['data']['bitrate'].append({
            'time': event['time'],
            'id': event['data']['to']['id'],
            'bitrate': event['data']['to']['bitrate']
        })

    return output


def output(output, data):
    if output == OutputType.Matplotlib:
        ax = data['ax']
        x_axis = []
        y_axis = []

        out_data = data['data']['bitrate']
        prev_y = 0
        x_axis.append(0)
        y_axis.append(0)
        for ev_data in out_data:
            x_axis.append(ev_data['time'])
            y_axis.append(prev_y)
            x_axis.append(ev_data['time'])
            y_axis.append(ev_data['bitrate'])

            prev_y = ev_data['bitrate']

        ax.set_ylabel('bitrate (bps)')
        ax.set_xlabel('time (ms)')
        ax.plot(x_axis, y_axis, markersize=1.5)

    return data
