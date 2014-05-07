#!/usr/bin/env python
# coding=utf-8

"""
Async. client for the weather service
"""

from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.internet.protocol import Protocol
from twisted.web.client import Agent
from twisted.web.http_headers import Headers

import constants

KEY = constants.KEY
URL = constants.URL

class BeginningPrinter(Protocol):
    def __init__(self, finished):
        self.finished = finished
        self.remaining = 1024 * 10
        self.data = ""

    def dataReceived(self, bytes):
        if self.remaining:
            display = bytes[:self.remaining]
            self.data += display
            #print 'Some data received:'
            #print display
            self.remaining -= len(display)

    def connectionLost(self, reason):
        print 'Finished receiving body:', reason.getErrorMessage()
        print 'data =', self.data
        self.finished.callback(self.data)

agent = Agent(reactor)

def cbRequest(response):
    print 'In cbRequest response = ', response
    finished = Deferred()
    response.deliverBody(BeginningPrinter(finished))
    return finished


def cbGetData(response):
    print 'In cbGetData response = ', response


def cbShutdown(ignored):
    reactor.stop()



def get_weather(town='haifa', key=KEY):
    url = URL.format(town, key)

    d = agent.request(
        'GET',
        url,
        Headers({'User-Agent': ['Twisted Web Client']}),
        None)
    return d



if __name__ == "__main__":
    print 'Haifa'
    r = get_weather()
    r.addCallback(cbRequest)
    r.addErrback(cbShutdown)
    r.addCallback(cbGetData)


    print 'Paris'
    r2 = get_weather('Paris')
    r2.addCallback(cbRequest)
    #r2.addBoth(cbShutdown)

    reactor.run()