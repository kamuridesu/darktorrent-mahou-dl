def similarity(s: str, to_compare: str):
    longer = s
    shorter = to_compare
    if len(longer) < len(shorter):
        longer = to_compare
        shorter = s
    longer_len = len(longer)
    if longer_len == 0:
        return 1.0
    return (longer_len - levenshtein_distance(longer, shorter)) / longer_len


def levenshtein_distance(s: str, ss: str):
    s = s.lower()
    ss = ss.lower()

    costs = [0] * (len(ss) + 1)
    for i in range(len(s) + 1):
        last_value = i
        for j in range(len(ss) + 1):
            if i == 0:
                costs[j] = j
                continue
            if j > 0:
                new_value = costs[j - 1]
                if s[i - 1] != ss[j - 1]:
                    new_value = min(new_value, last_value, costs[j]) + 1
                costs[j - 1] = last_value
                last_value = new_value
        if i > 0:
            costs[len(ss)] = last_value
    return costs[len(ss)]


FIREFOX_HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "en;q=0.5",
    "cache-control": "max-age=0",
    "dnt": "1",
    "sec-ch-ua": '"Brave";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "sec-gpc": "1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
}
