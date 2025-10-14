import os


def prepare_photo(path: str) -> dict[int, str]:
    directory = path
    result = {}
    total = 1

    for i in os.listdir(directory):
        result[total] = 'images/' + i
        total += 1

    return result