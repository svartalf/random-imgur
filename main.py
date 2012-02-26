# -*- coding: utf-8 -*-

import cherrypy
import jinja2
import redis

import settings

class Main(object):

    def __init__(self):
        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(settings.TEMPLATE_PATH))
        self.template = jinja_env.get_template('index.html')

        self.redis = redis.StrictRedis(db=settings.REDIS_DATABASE)

    @cherrypy.expose
    def index(self):
        key = None
        # TODO: if there really no images with 200 code, break cycle
        while 1:
            key = self.redis.randomkey()
            if not key:
                break

            value = self.redis.get(key)
            if value == '200':
                break

        return self.template.render(image=key.replace('.jpg', 'l.jpg'), url=key.replace('.jpg', '').replace('i.', ''))

if __name__ == '__main__':
    cherrypy.quickstart(Main())
else:
    application = cherrypy.Application(Main(), '')