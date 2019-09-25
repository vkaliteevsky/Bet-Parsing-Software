import socket
import urllib
import socks
import stem.process

from stem.util import term


class Tor:
    SOCKS_PORT = 7000
    tor_process = None
    socket = None
    socks = None

    def __init__(self):
        self.socks = socks
        self.socket = socket
        self.socks.setdefaultproxy(self.socks.PROXY_TYPE_SOCKS5, '127.0.0.1', self.SOCKS_PORT)
        self.socket.socket = self.socks.socksocket
        self.socket.getaddrinfo = self.get_address_info

    def get_address_info(self, *args):
        return [(self.socket.AF_INET, self.socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

    @staticmethod
    def query(url):
        try:
            return urllib.urlopen(url).read()
        except:
            return "Unable to reach %s" % url

    """
    Connect to the network with tor
    """
    def connect(self):
        self.tor_process = stem.process.launch_tor_with_config(config={'SocksPort': str(self.SOCKS_PORT)})

    """
    Close tor connection
    """
    def disconnect(self):
        self.tor_process.kill()

    """
    Change ip address
    """
    def reconnect(self):
        self.tor_process.kill()
        self.tor_process = stem.process.launch_tor_with_config(config={'SocksPort': str(self.SOCKS_PORT)})

    """
    Print current IP address
    """
    def print_ip(self):
        print term.format(self.query("http://my-ip.heroku.com"), term.Color.BLUE)