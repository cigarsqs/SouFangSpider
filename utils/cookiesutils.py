def get_cookies(raw_cookies):
    cookies = {}
    for line in raw_cookies.split(';'):
        key, value = line.split('=', 1)
        cookies[key] = value
    return cookies

