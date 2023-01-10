import matplotlib.pyplot as plt
import json

sent_packets = {}

with open('test.qlog', 'r') as file:
    header = file.readline()
    for entry in file:
        data = json.loads(entry)
        category, event_type = data['name'].split(':')

        if category == 'transport' \
        and event_type == 'packet_sent':
            packet_number = data['data']['header']['packet_number']
            if not packet_number in sent_packets:
                sent_packets[packet_number] = {}
            sent_packets[packet_number]['sent'] = data['time']
            sent_packets[packet_number]['size'] = data['data']['raw']['length']
        
        elif category == 'transport' \
        and event_type == 'packet_received':
            for frame in data['data']['frames']:
                if frame['frame_type'] == 'ack':
                    for ack_range in frame['acked_ranges']:
                        print(ack_range)
                        if len(ack_range) == 1:
                            sent_packets[ack_range[0]]['ack'] = data['time']
                        else:
                            for packet_number in range(ack_range[0], ack_range[1]+1):
                                print(ack_range[0], packet_number, ack_range[1])
                                sent_packets[packet_number]['ack'] = data['time']
                    #TODO use ack_delay?

x_axis = []
y_axis = []

for packet_number in sent_packets:
    instantaneous_throughput = 0

    data = sent_packets[packet_number]

    if 'size' in data and 'sent' in data and 'ack' in data:
        instantaneous_throughput = data['size'] / (data['ack'] - data['sent'])
    else:
        pass
        print(packet_number)
     
    x_axis.append(packet_number)
    y_axis.append(instantaneous_throughput)

plt.plot(x_axis, y_axis, 'bs')
plt.ylabel('instantaneous throughput')
plt.xlabel('packetnumber')
plt.show()