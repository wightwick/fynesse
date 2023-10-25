from spotipy import Spotify

def create_genre_dict_from_artist_uris(a_uris: list[str], sp: Spotify):
    artists = []
    chunk_size = 50
    for i in range(0, len(a_uris), chunk_size):
        chunk = a_uris[i:i + chunk_size]  # Get a chunk of 50 elements
        output_chunk = sp.artists(chunk)  # Apply your function
        artists.extend(output_chunk['artists'])

    genre_lookup_lists = [
        {a['uri']:a['genres']} for a in
        artists
    ]
    genre_lookup = {k: v for d in genre_lookup_lists for k, v in d.items()}
    return genre_lookup

def flat_genre_list_for_artist_uris(a_uris: list[str], genre_lookup: dict[str, str]):
    flat_genre_list = [
        item for sublist 
        in [genre_lookup[a] for a in a_uris]
        for item in sublist
    ]
    return list(set(flat_genre_list))