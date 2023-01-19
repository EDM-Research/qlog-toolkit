import json
import sys


def read_events(input):
    with open(input, 'r') as file:
        header = json.loads(file.readline())
        qlog_format = header['qlog_format']

        if qlog_format == "JSON":
            if len(header['traces']) > 1:
                print("qlog contains more than 1 trace:", input, file=sys.stderr)
            for trace in header['traces']:
                for event in trace['events']:
                    yield event

        elif qlog_format == "NDJSON":
            for event in file:
                yield json.loads(event)

        else:
            raise Exception("unsupported qlog format: ", qlog_format)
