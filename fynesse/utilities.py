import time

def flatten_list_of_lists(list_of_lists: list[list]) -> list:
    return [
        item for sublist
        in list_of_lists 
        for item in sublist
    ]

def flat_genre_list_for_artist_uris(a_uris: list[str], genre_lookup: dict[str, list]):
    flat_genre_list = flatten_list_of_lists( 
        [genre_lookup[a] for a in a_uris]
    )
    return list(set(flat_genre_list))

def src_set_from_images_list(images_list: list[dict[str, str]]) -> str:
    return ', '.join([
            f"{img['url']} {img['width']}w"
            for img in images_list
        ])

def token_expired(token_dict: dict) -> bool:
    return token_dict['expires_at'] <= time.time()

def add_token_expiry_time(token_dict: dict) -> dict:
    token_dict['expires_at'] = token_dict['expires_in'] + int(time.time())
    return token_dict 