# -*- coding: utf-8 -*-
import string

import cherrypy
import jinja2
import redis
import json

import settings

class Main(object):

    def __init__(self):
        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(settings.TEMPLATE_PATH))
        self.template = jinja_env.get_template('index.html')
        self.images_template = jinja_env.get_template('images.html')

        self.redis = redis.StrictRedis(db=settings.REDIS_DATABASE)

    @cherrypy.expose
    def index(self):
        image = self.redis.srandmember('imgur.200')

        context = {
            'image': image.replace('.jpg', 'l.jpg'),
            'url': image.replace('.jpg', '').replace('i.', ''),
            'amount': self.redis.scard('imgur.200'),
            'ga_account': settings.GOOGLE_ANALYTICS_ACCOUNT,
            'facebook_account': settings.FACEBOOK_ACCOUNT,
        }

        return self.template.render(context)

    @cherrypy.expose
    def random(self):
        image = self.redis.srandmember('imgur.200')

        return json.dumps({
            'image': image.replace('.jpg', 'l.jpg'),
            'url': image.replace('.jpg', '').replace('i.', ''),
        })

    @cherrypy.expose
    def images(self):
        images = []
        for image in [self.redis.srandmember('imgur.200') for _ in range(40)]:
            images.append({
                'image': image.replace('.jpg', 'm.jpg'),
                'url': image.replace('.jpg', '').replace('i.', ''),
            })

        return self.images_template.render({'images': images})

    @cherrypy.expose
    def images_more(self):
        return

if __name__ == '__main__':
    cherrypy.quickstart(Main())
else:
    application = cherrypy.Application(Main())