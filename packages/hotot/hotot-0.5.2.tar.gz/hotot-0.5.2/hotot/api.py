import os
import logging
import requests
from functools import partial

methods = {'GET': requests.get, 'POST': requests.post, 'PUT': requests.put}


def _api(method, host, port, logger, req, mask=None, params={}, **kwargs):
    try:
        if not host.startswith('http'):
            host = 'http://' + host
        api_url = '{}{}/{}'.format(host, ':{}'.format(port) if port else '', req)
        response = methods[method](api_url, params=params, **kwargs)
        code = response.status_code
        req_msg = '[{}] API request to {}:'.format(code, response.url)
        if code in [200, 201]:
            if code == 200:
                logger.info('{} Successful response!'.format(req_msg))
            elif code == 201:
                logger.info('{} Ressource created!'.format(req_msg))

            response = response.json()
            if mask:
                if isinstance(mask, str):
                    return [elt[mask] for elt in response]
                return [{k: v for k, v in elt.items() if k in mask} for elt in response]
            return response
        else:
            if code >= 500:
                msg = 'Server Error'
            elif code == 404:
                msg = 'URL not found'
            elif code == 401:
                msg = 'Authentication Failed'
            elif code == 400:
                msg = 'Bad Request'
            elif code >= 300:
                msg = 'Unexpected Redirect'
            logger.error('{} {}'.format(req_msg, msg))
            return None
    except requests.exceptions.ConnectionError:
        logger.exception('Connection error')
        return None


def api(method='GET', host='localhost', port='', logger=None, api_token=None):
    logging.basicConfig(level=logging.ERROR)
    logger = logger or logging.getLogger(__name__)
    return partial(_api, method,
                   os.environ.get(str(host), host),
                   os.environ.get(str(port), port),
                   logger,
                   headers={
                       **({'Authorization': 'Bearer {}'.format(api_token)} if api_token else {})
                   }
                   )
