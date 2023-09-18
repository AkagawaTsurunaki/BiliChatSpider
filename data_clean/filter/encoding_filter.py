import chardet

threshold_confidence = 0.95


def __detect_encoding(text):
    result = chardet.detect(text.encode())
    encoding = result['encoding']
    confidence = result['confidence']
    return encoding, confidence


def encoding_filter(data: list):
    filtered_data = []

    for reply in data:
        encoding, confidence = __detect_encoding(reply['post'])
        if (encoding != 'utf-8') or (not (encoding == 'utf-8' and confidence >= threshold_confidence)):
            continue

        encoding, confidence = __detect_encoding(reply['response'])
        if (encoding != 'utf-8') or (not (encoding == 'utf-8' and confidence >= threshold_confidence)):
            continue

        filtered_data.append(reply)

    return filtered_data
