def short_word_filter(data: list, threshold: int = 4):
    result = []
    for pair in data:
        post, res = pair['post'], pair['response']
        if len(post) > 4 and len(res) > 4:
            result.append(pair)

    return result
