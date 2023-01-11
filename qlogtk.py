import matplotlib.pyplot as plt
import json

sent_packets = {}
received_packets = {}

with open('test.qlog', 'r') as file:
    header = file.readline()
    for entry in file:
        data = json.loads(entry)
        category, event_type = data['name'].split(':')

        if category == 'transport' \
        and event_type == 'packet_received':

            packet_number = data['data']['header']['packet_number']
            if not packet_number in sent_packets:
                sent_packets[packet_number] = {}
            sent_packets[packet_number]['sent'] = data['time']
            sent_packets[packet_number]['size'] = data['data']['raw']['length']
        
            for frame in data['data']['frames']:
                if frame['frame_type'] == 'ack':
                    for ack_range in frame['acked_ranges']:
                        print(ack_range)
                        if len(ack_range) == 1:
                            received_packets[ack_range[0]]['ack'] = data['time']
                        else:
                            for packet_number in range(ack_range[0], ack_range[1]+1):
                                print(ack_range[0], packet_number, ack_range[1])
                                received_packets[packet_number]['ack'] = data['time']
                    #TODO use ack_delay?
        
        elif category == 'transport' \
        and event_type == 'packet_sent':

            packet_number = data['data']['header']['packet_number']
            if not packet_number in received_packets:
                received_packets[packet_number] = {}
            received_packets[packet_number]['sent'] = data['time']
            received_packets[packet_number]['size'] = data['data']['raw']['length']

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


sent_x_axis = []
sent_y_axis = []
received_x_axis = []
received_y_axis = []

sent_y_avg = []
received_y_avg = []
alpha = 0.5

for g in [[sent_packets, sent_x_axis, sent_y_axis, sent_y_avg],[received_packets, received_x_axis, received_y_axis, received_y_avg]]:
    packets = g[0]
    x_axis = g[1]
    y_axis = g[2]
    y_avg = g[3]
    c_avg = None
    for packet_number in packets:
        instantaneous_throughput = 0

        data = packets[packet_number]

        if 'size' in data and 'sent' in data and 'ack' in data:
            instantaneous_throughput = ((data['size']*8) / ((data['ack'] - data['sent'])/1000))/1000
        else:
            pass
            print(packet_number)
        
        x_axis.append(packet_number)
        y_axis.append(instantaneous_throughput)

        if c_avg == None:
            c_avg = instantaneous_throughput
        else:
            c_avg = ((1-alpha) * c_avg) + (alpha * instantaneous_throughput)
        y_avg.append(c_avg)

plt.figure(figsize=(14, 5))
plt.suptitle('packet throughput')
plt.subplot(121)
plt.title("sent")
plt.plot(sent_x_axis, sent_y_axis, 'bs', markersize=1.5)
plt.plot(sent_x_axis, sent_y_avg, 'r')
plt.ylabel('instantaneous throughput (Kbps)')
plt.xlabel('packetnumber')
plt.subplot(122)
plt.title("received")
plt.plot(received_x_axis, received_y_axis, 'bs', markersize=1.5)
plt.plot(received_x_axis, received_y_avg, 'r')
plt.ylabel('instantaneous throughput (Kbps)')
plt.xlabel('packetnumber')
plt.show()