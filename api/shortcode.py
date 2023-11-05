import shortuuid

def generate_unique_short_code():
    return shortuuid.ShortUUID().random(length=7)