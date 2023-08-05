
def shared_key(key):
    def join_key(s, o):
        return s[key] == o[key]
    return join_key