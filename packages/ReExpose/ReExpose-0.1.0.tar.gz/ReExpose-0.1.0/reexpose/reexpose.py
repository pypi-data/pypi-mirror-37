''' ReExpose HTTP basic auth endpoints as unauthenticated ones on localhost '''

#! /usr/bin/env python3

import argparse
import logging

import requests
from cachetools import TTLCache
from flask import Flask, Response
from gevent.pywsgi import WSGIServer
from yaml import safe_load

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(logging.StreamHandler())

def load_config(config_file):

    ''' Load config from open file handle '''

    config = safe_load(config_file)
    if 'log_level' in config:
        if not hasattr(logging, config['log_level'].upper()):
            LOGGER.error('log_level %s was not an attr of logging', config['log_level'])
        else:
            LOGGER.setLevel(config['log_level'].upper())

    LOGGER.info('Sites loaded: %d', len(config['sites']))

    return config

def app_setup(**kwargs):

    ''' Create endpoints based on config file. '''

    app = Flask(__name__)

    @app.route('/')
    def info():
        # pylint: disable=unused-variable
        return 'ReExpose'

    config = load_config(kwargs['config'])

    cache = TTLCache(maxsize=len(config['sites']),
                     ttl=config.get('cache_ttl_secs', 30))

    @app.route('/sites/<site_name>', defaults={'path': ''})
    @app.route('/sites/<site_name>/<path:path>')
    def render_site(site_name, path):
        # pylint: disable=unused-variable
        site = config['sites'].get(site_name, None)

        if not site:
            LOGGER.warning('Request for nonexistent site %s', site_name)
            return 'Site not found: {}'.format(site_name), 404

        url = site['url']
        if path:
            url += '/{}'.format(path)

        creds = (site['creds']['user'],
                 site['creds']['pass'])

        resp = cache.get(url, None)
        if not resp:
            resp = requests.get(url, auth=creds)
            cache[url] = resp

        if resp.status_code == 404:
            return '', resp.status_code

        flask_resp = Response(resp.text)
        flask_resp.headers = {**flask_resp.headers,
                              **resp.headers}

        return flask_resp, resp.status_code

    LOGGER.info('Setup complete')
    return app

def main():

    ''' Call setup functions & actually run the app. '''

    parser = argparse.ArgumentParser(
        description='ReExpose HTTP basic auth endpoints as unauthenticated ones'
    )
    parser.add_argument('--config', '-c', type=argparse.FileType('r'), help='Config file',
                        required=True)
    parser.add_argument('--port', '-p', type=int, help='Port to listen on', default=5000)
    args = parser.parse_args()

    app = app_setup(**vars(args))
    LOGGER.info('Starting app')
    WSGIServer(('127.0.0.1', args.port), app).serve_forever()
