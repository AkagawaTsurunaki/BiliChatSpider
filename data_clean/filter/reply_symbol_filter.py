def reply_symbol_filter(data: list):
    filtered_data = []
    for reply in data:
        new_reply = {
            'post': find(reply['post']),
            'response': find(reply['response'])
        }
        filtered_data.append(new_reply)

    return filtered_data


def find(string: str):
    if "回复 @" in string:
        tmp = string[4:]
        for i in range(0, len(tmp)):
            if tmp[i] in [':', "："]:
                return tmp[i + 1:]

    return string


def reply_symbol_filter_2(data):
    result = []

    for reply in data:
        if '回复 @' in reply['post']:
            continue
        if '回复 @' in reply['response']:
            continue
        result.append(reply)

    return result
