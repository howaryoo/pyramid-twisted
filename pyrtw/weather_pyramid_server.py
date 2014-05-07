#!/usr/bin/env python
# coding=utf-8

"""
Sync. client to the weather service incuded in a pyramid server

Caching with redis
and outpout simple HTML
"""


from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response


import weather
from temperature import Temperature

def get_weather(request):
	town = request.matchdict.get('town', 'Paris')
	temp_per = Temperature.get_by(city=town)
	temp = 0
	if temp_per:
		temp = temp_per.temperature
	else:
		d = weather.get_weather(town)
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


if __name__ == '__main__':
	config = Configurator()
	config.add_route('local_weather', '/weather/{town}')
	config.add_view(get_weather, route_name='local_weather')
	app = config.make_wsgi_app()
	server = make_server('0.0.0.0', 8888, app)
	server.serve_forever()