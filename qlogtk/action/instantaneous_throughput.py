from qlogtk.output import OutputType


def calculate(event, output):
    if output['data'] == {}:
        output['data']['sent'] = {}

    if event['category'] == 'transport' \
            and event['type'] == 'packet_sent':

        packet_number = event['data']['header']['packet_number']
        if not packet_number in output['data']['sent']:
            output['data']['sent'][packet_number] = {}
        output['data']['sent'][packet_number]['sent'] = event['time']
        output['data']['sent'][packet_number]['size'] = event['data']['raw']['length']

    elif event['category'] == 'transport' \
            and event['type'] == 'packet_received':

        packet_number = event['data']['header']['packet_number']

        for frame in event['data']['frames']:
            if frame['frame_type'] == 'ack':
                for ack_range in frame['acked_ranges']:
                    # print(ack_range)
                    if len(ack_range) == 1:
                        if not 'ack' in output['data']['sent'][ack_range[0]]:
                            output['data']['sent'][ack_range[0]
                                                   ]['ack'] = event['time']
                            output['data']['sent'][ack_range[0]]['throughput'] = ((output['data']['sent'][ack_range[0]]['size']*8) / (
                                (output['data']['sent'][ack_range[0]]['ack'] - output['data']['sent'][ack_range[0]]['sent'])/1000))  # bps
                    else:
                        for packet_number in range(ack_range[0], ack_range[1]+1):
                            # print(ack_range[0], packet_number, ack_range[1])
                            if not 'ack' in output['data']['sent'][packet_number]:
                                output['data']['sent'][packet_number]['ack'] = event['time']
                                output['data']['sent'][packet_number]['throughput'] = ((output['data']['sent'][packet_number]['size']*8) / (
                                    (output['data']['sent'][packet_number]['ack'] - output['data']['sent'][packet_number]['sent'])/1000))  # bps
                # TODO use ack_delay?

    return output


def output(output, data):
    if output == OutputType.Matplotlib:
        ax = data['ax']
        x_axis = []
        y_axis = []

        out_data = data['data']['sent']
        for x in out_data:
            ev_data = out_data[x]
            if 'throughput' in ev_data:
                x_axis.append(x)
                y_axis.append(ev_data['throughput'])

        ax.set_ylabel('throughput (Kbps)')
        ax.set_xlabel('packet number')
        ax.plot(x_axis, y_axis, 'bs', markersize=1.5)

    return data
