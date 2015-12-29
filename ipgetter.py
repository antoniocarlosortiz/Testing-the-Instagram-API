import re
import random
import signal
import urllib
import urllib2
import requests

#version tells the current version of python
from sys import version_info
from pprint import pprint
from functools import wraps

PY3K = version_info

__version__ = "0.5.2"

def timeout(seconds, error_message = "Function call timed out"):
    '''
    Decorator method that detects whether the subject function has timed out or not.
    '''
    def decorated(func):
        def __handle_timeout(signum, frame):
            print 'signal handler called with signal', signum
            #raise to explicitly call errors
            raise TimeOutError(error_message)
            print "Timeout! Timeout!"

        @wraps(func)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, __handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wrapper
    return decorated


@timeout(10)
def myip():
    return  IPgetter().get_externalip()


@timeout(10)
def myiptestaccuracy():
    return IPgetter().test()


class IPgetter(object):
    '''
    This class is designed to fetch your external IP addressm from the internet.
    It is used mostly when behind a NAT.
    It picks your IP randomly from a server list to minimize request overhead.
    '''

    def __init__(self):
        self.server_list = ['http://ip.dnsexit.com',
                            'http://ifconfig.me/ip',
                            'http://ipecho.net/plain',
                            'http://checkip.dyndns.org/plain',
                            'http://ipogre.com/linux.php',
                            'http://whatismyipaddress.com/',
                            'http://ip.my-proxy.com/',
                            'http://websiteipaddress.com/WhatIsMyIp',
                            'http://getmyipaddress.org/',
                            'http://www.my-ip-address.net/',
                            'http://myexternalip.com/raw',
                            'http://www.canyouseeme.org/',
                            'http://www.trackip.net/',
                            'http://icanhazip.com/',
                            'http://www.iplocation.net/',
                            'http://www.howtofindmyipaddress.com/',
                            'http://www.ipchicken.com/',
                            'http://whatsmyip.net/',
                            'http://www.ip-adress.com/',
                            'http://checkmyip.com/',
                            'http://www.tracemyip.org/',
                            'http://checkmyip.net/',
                            'http://www.lawrencegoetz.com/programs/ipinfo/',
                            'http://www.findmyip.co/',
                            'http://ip-lookup.net/',
                            'http://www.dslreports.com/whois',
                            'http://www.mon-ip.com/en/my-ip/',
                            'http://www.myip.ru',
                            'http://ipgoat.com/',
                            'http://www.myipnumber.com/my-ip-address.asp',
                            'http://www.whatsmyipaddress.net/',
                            'http://formyip.com/',
                            'https://check.torproject.org/',
                            'http://www.displaymyip.com/',
                            'http://www.bobborst.com/tools/whatsmyip/',
                            'http://www.geoiptool.com/',
                            'https://www.whatsmydns.net/whats-my-ip-address.html',
                            'https://www.privateinternetaccess.com/pages/whats-my-ip/',
                            'http://checkip.dyndns.com/',
                            'http://myexternalip.com/',
                            'http://www.ip-adress.eu/',
                            'http://www.infosniper.net/',
                            'http://wtfismyip.com/',
                            'http://ipinfo.io/',
                            'http://httpbin.org/ip']

    def get_externalip(self):
        '''
        This gets your IP from a random server.
        '''

        random.shuffle(self.server_list)
        myip = ''
        for server in self.server_list:
            myip = self.fetch(server)
            if myip != '':
                return myip
            else:
                continue
        return ''


    def fetch(self, server):
        '''
        This function gets your IP from a specifc server.
        '''
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36"
        headers = { "User-Agent" : user_agent}

        try:
            r = requests.get(server, headers=headers)
            content = r.content

            if PY3K:
                try:
                    content = content.decode('UTF-8')
                except UnicodeDecodeError:
                    content = content.decode('ISO-8859-1')
            m = re.findall(r'[0-9]+(?:\.[0-9]+){3}', content)
            myip = m[0]

            if len(myip) > 0:
                return myip
            else:
                return ''
        except Exception:
            return ''


    def test(self):
        '''
        This method tests the consistency of the servers on the list when retrieving your IP.
        All results should be the same to pass the test.
        '''

        resultdict = {}
        for server in self.server_list:
            print "checking %s" % server
            resultdict.update(**{server: self.fetch(server)})

        ips = sorted(resultdict.values())
        ips_set = set(ips)
        print "\nNumber of servers: {}".format(len(self.server_list))
        print "IP's : "

        #lambda x: ips.count(x)
        def a(x):
            return ips.count(x)

        #map(lambda x: ips.count(x), ips_set)
        b = [a(x) for x in ips_set]

        for ip, occurence in zip(ips_set, b):
            print '{0} = {1} occurenc{2}'.format(ip if len(ip) > 0 'broken server',
                                                  occurence,
                                                  'e' if occurence == 1 else 'es')

        print ""
        pprint(resultdict)

if __name__ == "__main__":
    test = IPgetter()
    test.test()

    print myip()




