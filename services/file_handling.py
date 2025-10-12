def prepare_news(path: str) -> dict[str]:
    result = {}

    file = open(path, encoding="utf-8")
    for i in file:
        i = i.rstrip()
        result[i[0]] = {i[3:i.find('|')]: i[i.find('|')+1:]}

    return result


