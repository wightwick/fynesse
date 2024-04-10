"""
Constants:
    Global logic constants
    Strings used throughout UI; in once place for easier modification
"""
LOGGING_ENABLED = False

NUM_RECCOMENDATIONS_DEFAULT = 10
NUM_SEARCH_RESULTS_DEFAULT = 10

SEARCH_RESULTS_TYPE_OPTIONS = ['tracks', 'artists']
SEARCH_RESULTS_TYPE_TRACKS = 'tracks'
SEARCH_RESULTS_TYPE_ARTISTS = 'artists'


SUB_PANE_WARNING_RED = 'rgb(235,104,91)'
SPOTIFY_API_SCOPES = [
    'user-read-playback-state',
    'user-modify-playback-state',
    'user-read-currently-playing',
    'app-remote-control',
    'playlist-read-private',
    'playlist-read-collaborative',
    'playlist-modify-public',
    'user-top-read',
    'user-read-recently-played',
    'user-library-modify',
    'user-library-read',
]

APP_NAME = 'fynesse'
APP_DESCRIPTION = 'Finesse your Spotify recommendations'

ACTIVE_DEVICE_NAME_TEXT = 'playback device: '
NO_ACTIVE_DEVICES_TEXT = 'no active devices for playback'

ACTIVE_DEVICE_REQUIRED_POPOVER_TEXT = 'active spotify device required to play multiple tracks'

LIBRARY_PANE_HEADER_TEXT = 'library'
RECOMMENDATIONS_PANE_HEADER_TEXT = 'recommendations'
SEARCH_PANE_HEADER_TEXT = 'search'

RESULTS_SUB_PANE_HEADER_TEXT = 'results'
RECC_TRACKS_SUB_PANE_HEADER_TEXT = 'recommended tunes'

SEEDS_SUB_PANE_HEADER_TEXT = 'seeds'
TOO_MANY_SEEDS_HEADER_TEXT = '5 seeds max'
PARAMETERS_SUB_PANE_HEADER_TEXT = 'parameters'

LIKED_SONGS_TAB_NAME_TEXT = 'liked songs'
PLAYLIST_TAB_NAME_TEXT = 'playlist'
RECENTLY_PLAYED_TAB_NAME_TEXT = 'recently played'
TOP_TAB_NAME_TEXT = 'top'

GERMINATE_HINT = 'germinate seeds to get recommendations'
SEARCH_HINT = 'type something above'
PLANT_SEEDS_HINT_TEXT = 'plant some seeds'

PLAY_ALL_TRACKS_BUTTON_TEXT = 'play all'
ARTIST_GENRES_BUTTON_TEXT = 'see artist genres'
LOAD_MORE_BUTTON_TEXT = 'load more'
SAVE_PLAYLIST_BUTTON_TEXT = 'save to playlist'
GENERATE_RECOMMENDATIONS_BUTTON_TEXT = 'germinate seeds 🪴'

PLAYLIST_CREATE_DIALOG_HEADER_TEXT = 'new playlist'
CREATE_PLAYLIST_BUTTON_TEXT = 'create playlist'

LISTEN_ON_SPOTIFY_TEXT = 'listen on Spotify'

AUTHENTICATE_DIALOG_HEADER_TEXT = 'log in with Spotify to use fynesse'
AUTHENTICATE_BUTTON_TEXT = 'log in'

TARGET_ACOUSTICNESS_SLIDER_TEXT = 'target acousticness'
TARGET_ENERGY_SLIDER_TEXT = 'target energy'
TARGET_LIVENESS_SLIDER_TEXT = 'target liveness'
TARGET_DANCEABILITY_SLIDER_TEXT = 'target danceability'
TARGET_INSTRUMENTALNESS_SLIDER_TEXT = 'target instrumentalness'
TARGET_VALENCE_SLIDER_TEXT = 'target valence (happiness)'
TARGET_TEMPO_INPUT_TEXT = 'target tempo'
TEMPO_RANGE_INPUT_NAME = 'tempo range'

NUM_RECOMMENDED_TRACKS_SLIDER_TEXT = 'number of recommended tracks: '

ACOUSTICNESS_DESC_TEXT = 'A confidence measure from 0.0 to 1.0 of whether the track is acoustic.'
ENERGY_DESC_TEXT = 'Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.'
LIVENESS_DESC_TEXT = 'Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.'
DANCEABILITY_DESC_TEXT = 'Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity.'
INSTRUMENTALNESS_DESC_TEXT = 'Predicts whether a track contains no vocals. "Ooh" and "aah" sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly "vocal". The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.'
VALENCE_DESC_TEXT = 'A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).'
TARGET_TEMPO_DESC_TEXT = 'Track tempo (BPM) to target in recommendations'
TEMPO_RANGE_DESC_TEXT = 'Hard limits on the minimum and maximum track tempo (BPM) of recommendations'

SEARCH_RESULTS_TYPE_RADIO_TEXT = 'results type:'
SEARCH_ARTIST_FIELD_TEXT = 'artist'
SEARCH_TRACK_FIELD_TEXT = 'track'
SEARCH_GENRE_FIELD_TEXT = 'genre'
SEARCH_YEAR_FIELD_TEXT = 'year'
NUM_SEARCH_RESULTS_SLIDER_TEXT = 'number of results: '

SPOTIFY_GREEN = '#1DB954'

