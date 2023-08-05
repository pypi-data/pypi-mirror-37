__version__ = '0.1.0'

# TODO:
#    - automatic credential fetching. Renew stale creds.
#    - change all to_exclude parameters to to_keep, so is explicit / can use in docs.
#    - general handling of a name query versus URI (e.g. via a decorator)
#    - need to remove albums artists are only contributers to, or add field?

import pandas as pd
from functools import partial
from itertools import chain

CONFIG_PATH = '~/.tidyspotify.yml'

COLS_EXCLUDE_TRACKS = ('artists', 'available_markets', 'external_urls', 'is_local', 'disc_number')


# Features that may be useful for analyses ----

FEATURES_TRACK = (
        'acousticness', 'danceability', 'energy', 'instrumentalness',
        'liveness', 'loudness', 'speechiness', 'valence', 'tempo', 'key',
        'time_signature'
        )

FEATURES_ALBUM = (
        'album_popularity', 'release_date'
        )

# Utils ---------------------------------------------------------------------------------

def is_uri(s):
    return True


def exclude_fields(to_exclude, d):
    return {k: v for k, v in d.items() if k not in to_exclude}


def keep_fields(to_keep, d):
    return {k: d[k] for k in to_keep if k in d}


def row_filter(fields, exclude = True):
    f = exclude_fields if exclude else keep_fields
    return partial(f, frozenset(fields))


def prefix_merge(left, right, prefix, *args, **kwargs):
    """Merge two dataframes, but prefix rather than suffix shared cols"""
    shared = set(left.columns).intersection(set(right.columns))
    new_left  = left.rename(columns = {x: prefix[0] + x for x in shared})
    new_right = right.rename(columns = {x: prefix[1] + x for x in shared})
    return new_left.merge(new_right, *args, **kwargs)


# Client --------------------------------------------------------------------------------
# note: this currently takes the hacky approach of having all functions use the 
#       client (sp) defined here

import spotipy
from spotipy import SpotifyException
from spotipy.oauth2 import SpotifyClientCredentials
from functools import wraps
from pathlib import Path
import yaml
import os

default_client = None


class FileCredentialManager(SpotifyClientCredentials):
    def __init__(self, client_id=None, client_secret=None, proxies=None):
        """Try Authenticating in this order: 
        
            1. client_id and secret args
            2. SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET enivronment variables
            3. ~/.tidyspotify.yml config file
        """

        p = Path(CONFIG_PATH).expanduser()

        if client_id or client_secret or os.environ.get('SPOTIPY_CLIENT_ID'):
            return super().__init__(client_id, client_secret, proxies)
        elif p.exists():
            config = yaml.load(p.open())
            return super().__init__(proxies = proxies, **config)
        else:
            return super().__init__()


def save_credentials(verify = True):
    """Login to spotify api. Saves credentials to file."""
    config = {
        'client_id': input('client id: '),
        'client_secret': input('client secret: ')
        }

    if verify:
        sp = spotipy.Spotify(client_credentials_manager = SpotifyClientCredentials(**config))
        try:
            sp.search("The Beatles")
        except SpotifyException as e:
            # TODO: informative message
            raise

    path = Path(CONFIG_PATH).expanduser()
    print("Writing credentials to %s" % path.absolute())

    yaml.dump(config, path.open('w'), default_flow_style = False)


def default_login():
    global default_client
    client_credentials_manager = FileCredentialManager()
    default_client = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return default_client


def login(f):
    @wraps(f)
    def wrapper(*args, client = None, **kwargs):
        if client is None:
            client = default_login() if default_client is None else default_client
        return f(*args, client = default_client, **kwargs)
    return wrapper

# API Main Entrypoints -------------------------------------------------------------------

@login
def get_artist_audio_features(q, interactive = False, genre_delimiter = '-!!-', to_file = '', client = None):
    """Return DataFrame with artist, album, and track data.
    
    Parameters:
        q: An artist to retrieve data for. 
        interactive: If true, prompts you to choose between similar artists.
        genre_delimiter: Collapse genre column into strings like "genre1-!!-genre2".
                      If set to None, keeps genres as a list for each row.
    """
    query = client.search(q = q, type = "artist")
    items = query['artists']['items']

    if not items:
        raise Exception("No artists found")

    if interactive:
        print("Select the artist to use...")
        print("\n".join("[{}]: {}".format(ii, entry['name']) for ii, entry in enumerate(items)))
        artist_indx = int(input("artist number: ").strip())
        if artist_indx > len(items):
            raise IndexError("Selected number higher than options available")
        artist = items[artist_indx]
    else:
        artist = items[0]

    # get artist genres
    artist_genres = genre_delimiter.join(artist['genres']) if genre_delimiter else None

    # get artist albums
    albums = get_artist_albums(artist['id'])
    albums['artist_genres'] = artist_genres

    # get album popularity
    album_popularity = get_album_popularity(albums.id)

    # get album tracks
    tracks = get_album_tracks(albums.id)

    # get track audio features
    features = get_track_features(tracks.id)

    # get track popularity
    popularity = get_track_popularity(tracks.id)

    album_data = albums.merge(album_popularity, 'left', 'id')

    track_data = tracks \
            .drop(columns = ['type']) \
            .merge(popularity, 'left', 'id') \
            .merge(features.drop(columns = ['uri', 'type', 'duration_ms']), 'left', 'id')


    merged = prefix_merge(album_data, track_data, ['album_', 'track_'], how = 'left', on = 'album_id')

    if to_file:
        merged.to_csv(to_file)

    return merged


@login
def get_recommendations(artists = tuple(), genres = tuple(), limit = 20, features = True, client = None):
    """Return DataFrame of recommended tracks.
    
    Arguments:
        artists: an optional sequence of artists to seed recommendation
        genres: an optional sequence of genres to seed recommendation
        limit: number of tracks to return
        features: whether to include track features in output
    """

    recs = client.recommendations(seed_artists = artists, seed_genres = genres, limit = limit)
    tracks = recs['tracks']

    # TODO: need a compose function...
    to_keep = (
            'album_name', 'artist_name', 'name', 'popularity', 'duration_ms',
            'explicit', 'id'
            )
    rows = list(map(row_filter(to_keep, False), map(_hoist_track_info, tracks)))
    out = pd.DataFrame(rows)

    track_ids = [row['id'] for row in rows]
    if features:
        extra_cols = ['uri', 'type', 'duration_ms', 'analysis_url', 'track_href']
        return out.merge(
                get_track_features(track_ids).drop(columns = extra_cols),
                on = "id"
                )

    return out
    
def _hoist_track_info(track):
    """Mutates track with artist and album info at top level."""
    track['album_name'] = track['album']['name']
    artist = track['artists'][0]
    track['artist_name'] = artist['name']
    return track


@login
def get_recommendation_genre_seeds(client = None):
    """Return genres that can be used in get_recommendations"""

    return client.recommendation_genre_seeds()['genres']


    

# API Functions -------------------------------------------------------------------------

@login
def get_artist_albums(
        artist_id, 
        to_exclude = ('available_markets', 'artists', 'external_urls', 'href', 
                      'images', 'type', 'uri', 'release_date_precision',
                      'album_group', 'total_tracks'),
        to_df = True,
        client = None):
    """Return albums belonging to an artist.
    
    Arguments:
        artist_id: artist uri or an artist name to search
        to_exclude: fields to exclude from each row of data
        to_df: return a DataFrame rather than a list

    """
    # artist_name artist_uri   album_uri   album_name     album_img        album_type is_collaboration

    if not is_uri(artist_id):
        query = client.search(q = artist_id, type = "artist")
        items = query['artists']['items']
        if not items:
            raise Exception("No artist matching search: %s" %artist_id)
        artist_id = items[0]['id']
    
    # TODO: pass args?
    albums = client.artist_albums(artist_id)
    row_filter(['id'])
    items = albums['items']
    for entry in items:
        artist = entry['artists'][0]
        entry['artist_name'] = artist['name']
        entry['artist_uri'] = artist['uri']

    data = list(map(row_filter(to_exclude), items))
    return pd.DataFrame(data) if to_df else data


@login
def get_album_popularity(album_ids, to_df = True, client = None):
    query = client.albums(album_ids)
    
    data = list(map(row_filter(['id','popularity'], exclude = False), query['albums']))

    return pd.DataFrame(data) if to_df else data
    

@login
def get_album_tracks(
        album_ids,
        to_exclude = COLS_EXCLUDE_TRACKS,
        to_df = True,
        client = None
        ):
    
    items = chain.from_iterable(map(lambda x: _get_album_tracks(x, client), album_ids))
    
    rows = list(map(row_filter(to_exclude), items))
    
    return pd.DataFrame(rows) if to_df else rows


def _get_album_tracks(album_id, client):
    items = client.album_tracks(album_id)['items']
    for item in items:
        item['album_id'] = album_id
        yield item


@login
def get_track_features(track_ids, to_df = True, client = None):
    tracks = []
    for ii in range(0, len(track_ids), 99):
        tracks.extend(client.audio_features(track_ids[ii:ii+99]))
    
    return pd.DataFrame(tracks) if to_df else tracks


@login
def get_track_popularity(track_ids, to_df = True, client = None):
    filter_entries = row_filter(['id', 'popularity'], exclude = False)
    
    tracks = []
    for ii in range(0, len(track_ids), 50):
        crnt_tracks = client.tracks(track_ids[ii:ii+50]).get('tracks', [])
        tracks.extend(map(filter_entries, crnt_tracks))
    
    return pd.DataFrame(tracks) if to_df else tracks


def main():
    from functools import update_wrapper
    import argh

    # hacky workaround due to: https://github.com/neithere/argh/issues/132
    # TODO: proper CLI implementation (using Click?)
    def to_csv(q, interactive = False, to_file = ''):
        return get_artist_audio_features(**locals())

    def get_recs(artists = tuple(), genres = tuple(), features = True):
        return get_recommendations(**locals())

    def get_genres():
        return get_recommendation_genre_seeds()

    update_wrapper(to_csv, get_artist_audio_features)
    update_wrapper(get_recs, get_recommendations)
    update_wrapper(get_genres, get_recommendation_genre_seeds)

    p = argh.ArghParser()
    p.add_commands([to_csv, get_recs, get_genres, save_credentials])
    p.dispatch()


if __name__ == '__main__':
    main()

