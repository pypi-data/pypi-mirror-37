from .config import *
from .API_util import make_request
import json


def get_tmdb_movie(title, year):
    """ Fetch data from TMdb API. """
    tmdb_url = 'https://api.themoviedb.org/3/search/movie?api_key=' + get_setting('API', 'TMdb_API_key') + '&'
    params = {'query': title.encode('ascii', 'ignore'),
              'language': 'en-US'}

    if year:
        params['year'] = year
    return make_request(tmdb_url, params, title)


def get_tmdb_details(id):
    tmdb_url = 'https://api.themoviedb.org/3/movie/' + str(id) + '?api_key=' + get_setting('API', 'TMdb_API_key') + '&'
    params = {'language': 'en-US'}
    return make_request(tmdb_url, params, 0)


def get_tmdb_genre(ids):
    if not os.path.exists(get_setting('Index', 'location') + 'tmdb_genre_list.json'):
        tmdb_url = 'https://api.themoviedb.org/3/genre/movie/list?api_key=' + get_setting('API', 'TMdb_API_key')
        genre_json = make_request(tmdb_url, {}, 0)
        with open(get_setting('Index', 'location') + 'tmdb_genre_list.json', "w") as out:
            json.dump(genre_json, out, indent=2)

    with open(get_setting('Index', 'location') + 'tmdb_genre_list.json') as genre_list:
        data = json.load(genre_list)

    for x in data['genres']:
        try:
            if ids[0] == x['id']:
                return x['name']
        except IndexError:
            return 'N/A'

