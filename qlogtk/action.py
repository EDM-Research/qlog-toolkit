def calculate_instantaneous_throughput(event, output):
    if output == {}:
        output['action'] = 'calculate_instantaneous_throughput'

    return output


def test(event, output):
    if output == {}:
        output['action'] = 'test'
        output['counter'] = 0
    output['counter'] += 1
    return output
