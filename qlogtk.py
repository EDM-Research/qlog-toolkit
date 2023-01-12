import json

sent_packets = {}
received_packets = {}

with open('test_s.qlog', 'r') as file:
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
                        # print(ack_range)
                        if len(ack_range) == 1:
                            received_packets[ack_range[0]]['ack'] = data['time']
                        else:
                            for packet_number in range(ack_range[0], ack_range[1]+1):
                                # print(ack_range[0], packet_number, ack_range[1])
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
                        # print(ack_range)
                        if len(ack_range) == 1:
                            if not 'ack' in sent_packets[ack_range[0]]:
                                sent_packets[ack_range[0]]['ack'] = data['time']
                        else:
                            for packet_number in range(ack_range[0], ack_range[1]+1):
                                # print(ack_range[0], packet_number, ack_range[1])
                                if not 'ack' in sent_packets[packet_number]:
                                    sent_packets[packet_number]['ack'] = data['time']
                    #TODO use ack_delay?


sent_x_axis = []
sent_y_axis = []
received_x_axis = []
received_y_axis = []

sent_y_avg = []
received_y_avg = []
alpha = 0.5

sent_lookup = {}
received_lookup = {}

for g in [[sent_packets, sent_x_axis, sent_y_axis, sent_y_avg,sent_lookup],[received_packets, received_x_axis, received_y_axis, received_y_avg,received_lookup]]:
    packets = g[0]
    x_axis = g[1]
    y_axis = g[2]
    y_avg = g[3]
    lookup = g[4]
    c_avg = None
    for packet_number in packets:
        instantaneous_throughput = 0

        data = packets[packet_number]

        if 'size' in data and 'sent' in data and 'ack' in data:
            instantaneous_throughput = ((data['size']*8) / ((data['ack'] - data['sent'])/1000))/1000
        else:
            pass
            print(packet_number)
        
        x = data['sent']
        y = instantaneous_throughput
        x_axis.append(x)
        y_axis.append(y)
        if not (x,y) in lookup:
            lookup[(x,y)] = []
        lookup[(x,y)].append(packet_number)

        if c_avg == None:
            c_avg = instantaneous_throughput
        else:
            c_avg = ((1-alpha) * c_avg) + (alpha * instantaneous_throughput)
        y_avg.append(c_avg)

import matplotlib.pyplot as plt
import sys

fig, (plot1, plot2) = plt.subplots(1,2, sharex=True, sharey=True)
fig.suptitle('packet throughput')

plot1.set_title("sent")
plot1line, = plot1.plot(sent_x_axis, sent_y_axis, 'bs', markersize=1.5, picker=True)
plot1line.set_gid("plot1")
plot1.set_ylabel('instantaneous throughput (Kbps)')
plot1.set_xlabel('time (ms)')

plot2.set_title("received")
plot2line, = plot2.plot(received_x_axis, received_y_axis, 'bs', markersize=1.5, picker=True)
plot2line.set_gid("plot2")
plot2.set_ylabel('instantaneous throughput (Kbps)')
plot2.set_xlabel('time (ms)')

annotation = None

def on_pick(event):
    obj = event.artist
    xdata = obj.get_xdata()
    ydata = obj.get_ydata()
    ind = event.ind
    points = tuple(zip(xdata[ind], ydata[ind]))
    lookup = None
    plot = None
    if obj.get_gid() == "plot1":
        lookup = sent_lookup
        plot = plot1
    elif obj.get_gid() == "plot2":
        lookup = received_lookup
        plot = plot2
    else:
        print("bad gid")
        return
    
    annotation_text = ""
    min = sys.maxsize
    max = -sys.maxsize
    for i in range(len(points)):
        for p in lookup[points[i]]:
            if p < min:
                min = p
            if p > max:
                max = p
    if min == max:
        annotation_text = str(min)
    else:
        annotation_text = str(min) + "..." + str(max)
    print(annotation_text)

    global annotation
    if not annotation is None:
        annotation.remove()

    annotation = plot.annotate(annotation_text, xy=points[0],  xycoords='data',
            xytext=(0.8, 0.95), textcoords='axes fraction',
            arrowprops=dict(facecolor='black', shrink=0.05),
            horizontalalignment='right', verticalalignment='top',
            )
    
    plt.draw()

fig.canvas.mpl_connect("pick_event", on_pick)
plt.show()