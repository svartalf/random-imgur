# -*- coding: utf-8 -*-

"""Check random image code for existence"""

import time
import redis
import requests
import logging

import settings
import helpers

class ImageChecker(object):

    def __init__(self):
        self.redis = redis.StrictRedis(db=settings.REDIS_DATABASE)
        logging.basicConfig(level=logging.DEBUG)

        self._headers = {
            'User-Agent': 'random-imgur/0.1 (https://github.com/svartalf/random-imgur)',
        }

        self._run = False

    def serve_forever(self):
        self._run = True
        while self._run:
            code = helpers.random_code()
            url = 'http://i.imgur.com/%s.jpg' % code
            response = requests.head(url)

            # Because imgur does'nt sends 404 for not-existent image, check for 404 image
            if response.headers['content-length'] == '669' and response.headers['content-type'] == 'image/gif':
                # TODO: maybe we should check image content?
                logging.debug('%s: 404' % url)
                self.redis.set(url, 404)
            else:
                logging.debug('%s: 200' % url)
                self.redis.set(url, 200)

            time.sleep(settings.CHECKER_INTERVAL)

    def stop(self):
        self._run = False

if __name__ == '__main__':
    checker = ImageChecker()
    try:
        checker.serve_forever()
    except KeyboardInterrupt:
        checker.stop()