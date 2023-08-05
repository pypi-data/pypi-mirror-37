import logging
import re
from multiprocessing.pool import ThreadPool
from typing import List

import html2text
import requests
from bs4 import BeautifulSoup
from django.core.cache import cache
from requests import Session, Request
from requests.cookies import cookiejar_from_dict
from requests.utils import dict_from_cookiejar

from . import parsers
from .models import Credentials
from .utils import QUERY_MAX_LENGTH, VIVA_COOKIES_CACHE_KEY

logger = logging.getLogger(__name__)
session = Session()

SEARCH_URL = 'https://www.viva-afrikaans.org/media/mod_viva_afrikaans/server/api.php?route=search&headword={}'
API_URL = 'https://www.viva-afrikaans.org/media/mod_viva_afrikaans/server/api.php'
LOGIN_URL = 'https://www.viva-afrikaans.org/user-teken-in'

TRANSLATION = {
    1: 'Afrikaans',
    3: 'Sepedi',
    4: 'Xitsonga',
    5: 'Setswana',
    6: 'IsiZulu'
}

BLACKLIST = [
    # 'ctext_lex',
    # 'aws_woordelys',   # AWS 2009, similar to aws_2017
]


def validate_query(q: str):
    q = q.strip()
    if not q:
        return False, 'Empty query: provide non-empty string'
    if q:
        if len(q) > QUERY_MAX_LENGTH:
            return False, f'Query too long: max {QUERY_MAX_LENGTH} characters'

    return True, ''


def query(q: str, include_raw=False):
    q = q.strip()

    pool = ThreadPool(2)
    results = []
    kwargs = {'include_raw': include_raw}

    def merge(x):
        nonlocal results
        results += x

    pool.apply_async(vertaal, (q,), kwargs, callback=merge)
    pool.apply_async(viva, (q,), kwargs, callback=merge)
    pool.close()
    pool.join()

    return add_text(results)


def add_text(results):
    parser = html2text.HTML2Text(bodywidth=0)
    parser.ignore_emphasis = True
    parser.ignore_links = True
    parser.ignore_images = True

    for result in results:
        markup = result.get('markup', '')
        text = parser.handle(markup)
        text = re.sub(r'([\n]{3,})', '\n\n', text.strip(), 0)
        result['text'] = text

    return results


def viva(q, include_raw=False):
    search_data = viva_search(q=q)
    reqs = []
    for source in search_data:
        params = dict(route=source['key'], headword=source['headword'])
        reqs.append(Request('GET', API_URL, params=params))

    responses = get_many_json(reqs)
    results = []
    for data, source_data in zip(responses, search_data):

        status = data.get('status', 200)
        if status == 404:
            continue
        source = data['route']
        parser = getattr(parsers, source, None)
        markup = ''
        if parser is not None:
            try:
                markup = parser(data)
            except (KeyError, AttributeError, ValueError) as e:
                logger.warning(f'[{source}] Parsing error: {e}')

        result = {
            'source': source_data['title'],
            'markup': markup,
        }

        if include_raw:
            result['raw'] = data

        results.append(result)
    return results


def viva_search(q):
    """
    Performs the initial search request that indicates which sources have results.
    :param q: The search term
    :return: A list of dicts with keys:
     key - the source slug
     title - title of the source
     count - the amount of results
    """
    data = get_json(SEARCH_URL.format(q))
    if 'status' in data and data['status'] in (401, 403):
        logger.info(f'[viva] status code {data["status"]}')
        # not logged in
        login()
        data = get_json(SEARCH_URL.format(q))
        if 'status' in data and data['status'] in (401, 403):
            logger.error(f'[viva] received status code "{data["status"]}" after login.')
            logger.error(data)
            return []
    if 'status' in data and data['status'] == 404:
        return []

    rv = []
    for result in data['results'][0]['results']:
        count = result.get('found', 0)
        if count == 0:
            continue
        key = result.get('dataset')
        if key in BLACKLIST:
            continue
        rv.append({
            'count': count,
            'key': result.get('dataset'),
            'title': result.get('label'),
            'headword': result.get('headword'),
        })
    return rv


def update_session_cookies():
    cookies = cookiejar_from_dict(cache.get(VIVA_COOKIES_CACHE_KEY))  # None is OK
    session.cookies.update(cookies)


def get_json(url, **kwargs):
    update_session_cookies()
    r = session.get(url, **kwargs)
    # do not call raise_for_status as response code is checked for login state
    return r.json()


def get_json_req(req: Request):
    r = session.send(session.prepare_request(req))
    return r.json()


def get_many_json(reqs: List[Request]):
    update_session_cookies()
    pool = ThreadPool(len(reqs))
    return pool.map(get_json_req, reqs)


def vertaal(q, include_raw=False):
    reqs = []
    for target in TRANSLATION.keys():
        params = dict(sourceid=1, targetid=target, text=q)
        reqs.append(Request('GET', 'http://mt.nwu.ac.za/services/translate/sentence', params=params))

    responses = get_many_json(reqs)
    results = []
    for response, lang in zip(responses, TRANSLATION.values()):
        if not response:
            continue
        if '_status' in response and response['_status'] != 200:
            continue
        markup = response.get('_message')
        if markup == q or markup.rstrip('.') == q:
            # when no results are found it returns the original query
            continue
        result = {
            'markup': response.get('_message'),
            'source': f'NWU Vertaler: {lang}'
        }
        if include_raw:
            result['raw'] = response
        results.append(result)

    return results


def login():
    credentials = Credentials.objects.filter(active=True).first()
    url = 'https://www.viva-afrikaans.org/user-teken-in'
    blank_session = Session()
    r = blank_session.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    values = {i.attrs.get('name'): i.attrs.get('value') for i in soup.select('.form-login-username input')}
    values['username'] = credentials.username
    values['password'] = credentials.password
    params = {'task': 'user.login'}
    logger.info(f'[viva] logging in with username {credentials.username}')
    try:
        r = blank_session.post(url=url, data=values, params=params)
        r.raise_for_status()
    except requests.RequestException as e:
        logger.warning(e)
        return False
    cookies = dict_from_cookiejar(blank_session.cookies)
    cache.set(VIVA_COOKIES_CACHE_KEY, cookies, None)
    logger.info('[viva] updated cookies in cache')
    return True
