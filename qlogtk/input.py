import json
import sys


def read_events(input):
    with open(input, 'r') as file:
        qlog_format = None
        qlog = None
        try:
            qlog = json.load(file)
            qlog_format = qlog['qlog_format']
        except:
            file.seek(0)
            qlog = json.loads(file.readline())
            qlog_format = qlog['qlog_format']
        finally:
            if qlog_format == "JSON":
                if len(qlog['traces']) > 1:
                    print("qlog contains more than 1 trace:", input, file=sys.stderr)
                for trace in qlog['traces']:
                    for event in trace['events']:
                        yield event

            elif qlog_format == "NDJSON":
                for event in file:
                    yield json.loads(event)

            else:
                raise Exception("unsupported qlog format: ", qlog_format)


def format_event(event):
    if 'name' in event:
        category, event_type = event['name'].split(':')
        event['category'] = category
        event['type'] = event_type

    return event