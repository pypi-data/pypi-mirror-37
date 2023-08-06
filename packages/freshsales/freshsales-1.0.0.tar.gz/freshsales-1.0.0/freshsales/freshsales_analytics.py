from .request import _request
from .freshsales_exception import FreshsalesException

class FreshsalesAnalytics(object):
    def __init__(self, domain=None, app_token=None):
        self.domain = domain
        self.app_token = app_token

    def identify(self, identifier=None, properties={}):
        data = {}
        data['identifier'] = identifier
        data['visitor'] = properties
        self._post('visitors', data)

    def trackEvent(self, identifier=None, event=None, properties={}):
        properties['name'] = event
        data = {}
        data['identifier'] = identifier
        data['event'] = properties
        self._post('events', data)

    def trackPageView(self, identifier=None, url=None):
        data = {}
        data['identifier'] = identifier
        data['page_view'] = { 'url': url }
        self._post('page_views', data)

    def _post(self, action, data):
        if self._valid(action, data):
            data['application_token'] = self.app_token
            data['sdk'] = "python"
            path = self.domain + '/track/' + action
            _request(path, data)

    def _valid(self, action, data):
        if not self.domain or not self.app_token:
            raise  FreshsalesException("Either Freshsales domain / appToken "
                   + "you provided during the initialization of FreshsalesAnalytics is empty.")
        elif not data['identifier']:
            raise  FreshsalesException("Identifier passed is empty")
        elif action == 'page_views' and not data['page_view']['url']:
            raise  FreshsalesException("Page URL passed to trackPageView method is empty.")
        elif action == 'events' and not data['event']['name']:
            raise  FreshsalesException("Event Name passed to trackEvent method is empty.")

        return True
