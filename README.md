# spotifind

:seedling: Advanced recommendation and search interface for spotify.

:package: UI written in [Reflex](https://github.com/reflex-dev/reflex/), Spotify API calls via [Spotipy](https://github.com/spotipy-dev/spotipy)


## Connecting to Spotify API and running the app

The core functionality of spotifind requires a connection to Spotify's web API.

To set this up:
1. Go to the [Spotify developer dashboard](https://developer.spotify.com/dashboard/applications)
1. Click `Create an app`
    - You now can see your `Client ID` and `Client Secret`
1. Click `Edit Settings`
1. Add `http://localhost:1234` to the Redirect URIs (or a port of your choice)
1. Scroll down and click `Save`
1. Add your `Client ID` and `Client Secret` to [sp_secrets.py](sp_secrets.py)
1. You are now ready to run the app. Do so by running `reflex init` followed by `reflex run` in the [parent directory](/)
1. On first run, a browser window will open to a spotify authentication page. When you accept, you will be redirected to a URL beginning `http://localhost:1234` (if you kept default port)
1. The terminal session in which reflex is running will prompt you to `Enter the URL you were redirected to`; copy-paste the redirect url from your browser's address bar into the terminal and press enter.
1. The app will start up!