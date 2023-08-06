from .data_models import data_models

import requests
from requests.adapters import HTTPAdapter
import ssl
import urllib.parse


class Adapter(HTTPAdapter):

    def __init__(self, settings):
        self.settings = settings
        super().__init__()

    def create_ssl_context(self, settings):

        ctx = ssl.create_default_context()
        # allow aes 128 cbc
        if 'ciphers' in settings:
            ctx.set_ciphers(settings['ciphers'])
        # allow TLS 1.0 and TLS 1.2 and later (disable SSLv3 and SSLv2)
        for option in settings['options']:
            if option == 'NO_SSLv2':
                ctx.options |= ssl.OP_NO_SSLv2
            elif option == 'NO_SSLv3':
                ctx.options |= ssl.OP_NO_SSLv3

        ctx.check_hostname = False
        return ctx

    def init_poolmanager(self, *args, **kwargs):
        kwargs['ssl_context'] = self.create_ssl_context(self.settings)
        return super(Adapter, self).init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        kwargs['ssl_context'] = self.create_ssl_context(self.settings)
        return super(Adapter, self).proxy_manager_for(*args, **kwargs)




class fhir_client():

    def __init__(self, settings):

        # FHIR settings
        if 'fhir' in settings and 'base_url' in settings['fhir']:
            self.fhir_base = settings['fhir']['base_url']
        else:
            exit(1)

        # HTTP settings
        if 'http' in settings and 'timeout' in settings['http']:
            self.http_timeout = settings['http']['timeout']
        else:
            self.http_timeout = 5


        # Create session
        self.session = requests.Session()

        # SSL settings
        if 'ssl' in settings and 'verify' in settings['ssl']:
            # May be True, False or path to a CA bundle or directory containing it.
            self.session.verify = settings['ssl']['verify']

        # SSL adapter
        if 'ssl' in settings and ('ciphers' in settings['ssl'] or 'options' in settings['ssl']):
            self.session.mount(self.fhir_base, Adapter(settings['ssl']))

        # Authorization settings
        if 'auth' in settings and 'authorization_header' in settings['auth']:
            self.session.headers.update({'Authorization': settings['auth']['authorization_header']})


    def read(self, resource_type, resource_id):

        r = self.session.get(
            url=self.fhir_base + '/' + resource_type + '/' + resource_id,
            timeout=self.http_timeout
        )

        if r.status_code == 200:
            return r.json()
        else:
            return None

    def create(self, resource):
        if data_models().validate(resource):

            r = self.session.post(
                url=self.fhir_base + '/' + resource['resourceType'],
                json=resource,
                timeout=self.http_timeout
            )

            if r.status_code == 201:
                return True
            else:
                return None

        else:
            return None

    def update(self):
        pass

    def delete(self):
        pass

    def search(self, resource_type, filter):

        r = self.session.get(
            url=self.fhir_base + '/' + resource_type + '?' + urllib.parse.urlencode(filter),
            timeout=self.http_timeout
        )

        if r.status_code == 200:
            return r.json()
        else:
            return None