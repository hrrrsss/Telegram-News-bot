def prepare_news(path: str) -> dict[str]:
    result = {}

    with open (path, "r", encoding="utf-8") as f:
        for i in f:
            i = i.rstrip()
            result[int(i[0])] = {i[3:i.find('|')-1]: i[i.find('|')+1:]}

    return result