from movielst import config
import requests
import os

dep_folder = config.CONFIG_PATH + 'dep/'
dependencies = ['https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
                'https://code.jquery.com/jquery-3.3.1.slim.min.js',
                'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js',
                'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js']


def check_for_dep():
    if not os.path.exists(dep_folder):
        os.makedirs(dep_folder)
    for url in dependencies:
        if not os.path.exists(dep_folder + url.rsplit('/', 1)[-1]):
            download_dep(url)


def download_dep(url):
    local_filename = url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(dep_folder + local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return local_filename
