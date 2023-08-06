import requests
from urllib.parse import urlencode
import json
import logging

logger = logging.getLogger(__name__)


def make_request(url, params, title):
    url = url + urlencode(params)
    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        r.status_code = "Connection refused"
    if r.status_code == 200:
        if "application/json" in r.headers['content-type']:
            return json.loads(r.text)
        else:
            print("Couldn't find the movie " + title)
            logger.info('[API] Movie could not be found: ' + title)
            return None
    elif r.status_code == 401:
        print("Invalid API key, please check config file.")
        logger.error('[API] Invalid key.')
        return None
    else:
        print("There was some error fetching info from " + url)
        logger.error('[API] Error fetching info from: ' + url)
        return None
