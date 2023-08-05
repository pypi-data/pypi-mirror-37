from pykospacing import spacing

def word_spacing(text):
    limit = 190
    result = ''
    split_temp = text.splitlines()

    for split in split_temp:
        split_with_limit_temp = [split[i: i + limit] for i in range(0, len(split), limit)]
        for split_with_limit in split_with_limit_temp:
            spacing_result = spacing(split_with_limit)
            result += spacing_result
        result += '\n'

    return result
