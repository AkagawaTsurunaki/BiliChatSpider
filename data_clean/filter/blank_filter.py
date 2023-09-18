def blank_filter(data: list):
    result = []
    for reply in data:
        if reply['post'] == '' or reply['response'] == '':
            continue
        result.append(reply)

    return result
