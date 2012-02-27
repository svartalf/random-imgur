# -*- coding: utf-8 -*-

import cherrypy
import jinja2
import redis
import json

import settings

class Main(object):

    def __init__(self):
        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(settings.TEMPLATE_PATH))
        self.template = jinja_env.get_template('index.html')

        self.redis = redis.StrictRedis(db=settings.REDIS_DATABASE)

    @cherrypy.expose
    def index(self):
        image = self.redis.srandmember('imgur.200')

        context = {
            'image': image.replace('.jpg', 'l.jpg'),
            'url': image.replace('.jpg', '').replace('i.', ''),
            'amount': self.redis.scard('imgur.200'),
        }

        return self.template.render(context)

    @cherrypy.expose
    def random(self):
        image = self.redis.srandmember('imgur.200')

        return json.dumps({
            'image': image.replace('.jpg', 'l.jpg'),
            'url': image.replace('.jpg', '').replace('i.', ''),
        })

if __name__ == '__main__':
    cherrypy.quickstart(Main())
else:
    application = cherrypy.Application(Main())