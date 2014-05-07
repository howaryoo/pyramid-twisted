#!/usr/bin/env python
# coding=utf-8

"""
Pyramid WSGI application 
intended to be used with twisd to make async calls to the weather service.
Redis is used to cache the data.

Ref: http://stackoverflow.com/questions/13122519/serving-pyramid-application-using-twistd


Start server with: 

⟫ ~/pyenv/bin/twistd web --port 9999 --wsgi twto.myApp


Usage:

http://localhost:9999/weather/paris




Interesting discussion about the subject:
http://twistedmatrix.com/pipermail/twisted-python/2012-May/025563.html

Quote:
Django is intended to be used in a multi-threaded (or multi-process) 
environment, not an asynchronous one.  It can't take advantage of 
Twisted's single-threaded asynchronous APIs (eg Deferreds). 

"""

import json
from pyrtw.temperature import Temperature

from pyramid.config import Configurator
from pyramid.response import Response
from twisted.internet import reactor, threads

import weather_async


def cbGetData(response):
    return response


def get_weather_async(town):
    d = weather_async.get_weather(town)

    d.addCallback(weather_async.cbRequest)
    d.addErrback(weather_async.cbShutdown)
    d.addCallback(cbGetData)
    return d
 
def get_weather(request):
    town = request.matchdict.get('town', 'Paris')

    temp_per = Temperature.get_by(city=town)
    temp = 0
    if temp_per:
        temp = temp_per.temperature
    else:
        result = threads.blockingCallFromThread(
            reactor, get_weather_async, town)
        d = json.loads(result)
        temp = d[u'data'][u'current_condition'][0][u'temp_C']
        temp_per = Temperature(city=town, temperature=temp)
        temp_per.save()
            

    return Response("""
<div style="text-align: center">
    <div style="font-size: 72px">{}</div>
    <div style="font-size: 144px">{}°C</div>
    <div style="font-size: 24px">Current temperature</div>
</div>"""\
    .format(town, temp))   

"""
def get_weather(request):
    town = request.matchdict.get('town', 'Paris')
    d = weather_async.get_weather(town)

    d.addCallback(weather_async.cbRequest)
    d.addErrback(weather_async.cbShutdown)
    d.addCallback(cbGetData)

    return Response('tata')
"""


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')

    config.add_route('local_weather', '/weather/{town}')
    config.add_view(get_weather, route_name='local_weather')
    
    
    config.scan()
    return config.make_wsgi_app()
