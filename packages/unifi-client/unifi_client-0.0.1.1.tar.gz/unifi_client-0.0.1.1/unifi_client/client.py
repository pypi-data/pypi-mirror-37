
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


class AirMaxAPIClient(object):
    def __init__(self, **kwargs):
        '''
            Args:
                :username (str): Username for login
                :password (str): Password for login
                :url (str): Weburl for the unifi Airmax
                :verify (bool): Verify certs
                :proxy (str): Set proxy path
            Returns:
                :AirMaxAPIClient (object): 

        '''
        self.username = kwargs['username']
        self.password = kwargs['password']
        self.url = kwargs['url']
        self.verify = kwargs.get('verify', True)
        proxy = kwargs.get('proxy', None)
        self.proxies = None
        if proxy:
            self.proxies = {
                'http': proxy,
                'https': proxy
            }
        self.session = None

    def path(self, path):
        '''
            builds up the complete URL

            Args:
                :path (str): Ressource extension
                :path (list): list of separated Ressource extensions

            Returns:
                :url (str): '<self.url/path>'
        '''

        return urljoin(self.url, path)

    def login(self):
        '''
            Login to the unifi AirMax Device
            Setup the session

            Returns:
                :status (bool): True success False failure
        '''
        self.session = requests.Session()
        self.session.proxies = self.proxies
        self.session.verify = self.verify
        url = self.path('api/auth')
        params = {
            'username': self.username,
            'password': self.password
        }
        login = self.session.post(url, data=params)
        return login.ok

    def logout(self):
        '''
            Logout the unifi AirMax Device
            Reset the session

            Returns:
                :status (bool): True success False failure
        '''
        if not self.session:
            raise Exception("You need to login")
        url = self.path('logout.cgi')
        logout = self.session.post(url)
        self.session = None
        return logout.ok

    def statistics(self):
        '''
            Get the statistics from the device

            Return:
                :statistics (dict): Device specific statistics
        '''
        if not self.session:
            raise Exception("You are not logged in.")
        url = self.path('status.cgi')
        response = self.session.get(url)
        return response.json()
