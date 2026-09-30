import requests
import pandas as pd

class Interface:
    def __init__(self, url, config, observer=None):
        self.url = url
        self.config = config
        self.observer = observer
        self._response = None

    @property
    def response(self):
        if not self._response:
            self._response = requests.get(self.url, params=self.params).json()
        return self._response 

class SB_Interface(Interface):
    _params = {'sb-kind':'a', 'two-pass':'true'}

    @property
    def params(self):
        rh, rm, rs = self.observer.ra.hms
        ra_str = f"{rh:02.0f}-{rm:02.0f}-{rs:05.2f}"
        dh, dm, ds = self.observer.dec.dms
        dec_str = f"{dh:02.0f}-{dm:02.0f}-{ds:05.2f}"
        self._params['fov-ra-center'] = ra_str
        self._params['fov-dec-center'] = dec_str
        self._params.update(self.config)
        return self._params

    @property
    def data(self):
        fields = self.response['fields_second']
        data = self.response['data_second_pass']
        df = pd.DataFrame(data, columns=fields)
        return df
        

class IP_Interface(Interface):
    _params = {}

    @property
    def params(self):
        self._params.update(self.config)
        return self._params

    @property
    def data(self):
        return
