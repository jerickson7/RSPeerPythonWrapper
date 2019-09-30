import requests
import json
from requests.exceptions import HTTPError


class BotManager:
    URL_BASE = "https://services.rspeer.org/api/botLauncher/"
    DEFAULT_JVM = "-Xmx768m -Djava.net.preferIPv4Stack=true -Djava.net.preferIPv4Addresses=true -Xss2m"

    def __init__(self, api_key):
        self._api_key = api_key

    def _do_request(self, path, data=None):
        url = self.URL_BASE + path
        headers = {'Content-Type': 'application/json',
                   'ApiClient': self._api_key}
        try:
            if data is None:
                resp = requests.get(url, headers=headers)
            else:

                resp = requests.post(url, headers=headers, data=json.dumps(data))

        except HTTPError as h:
            print(f"HTTP Error {h}")
        except Exception as err:
            print(f"Other exception {err}")
        else:
            if len(resp.text) > 0:
                return json.loads(resp.text)

    def launch_client(self, launcher, qs=None, proxy=None, jvm_args=DEFAULT_JVM, sleep=10, count=1):
        dat = {
            'payload': {
                'type': "start:client",
                'session': self._api_key,
                'qs': qs,
                'proxy': proxy,
                'jvmArgs': jvm_args,
                'sleep': sleep,
                'count': count
            },
            'socket': launcher
        }

        return self._do_request('send', data=dat)

    def get_launchers(self):
        return self._do_request('connected')

    def get_clients(self):
        return self._do_request('connectedClients')

    def get_proxies(self):
        return self._do_request('getProxies')

    def add_proxy(self, ip, name, password, port, username):
        dat = {
            'ip': ip,
            'name': name,
            'password': password,
            'port': port,
            'username': username
        }
        return self._do_request('saveProxy', data=dat)

    def delete_proxy(self, proxy_id):
        return self._do_request('deleteProxy?id=' + proxy_id, data={})  # Empty data to make it a post


if __name__ == '__main__':
    api_key = "paste ur key in"
    b = BotManager(api_key)
    launchers = b.get_launchers()
    proxies = b.get_proxies()

    # Launcher id's returned as keys.
    s = list(launchers.keys())[0]  # assuming you have at least one launcher open.
    launch_script = {
        'name': "a",
        'clients': {
            0: {
                "script": {
                    "scriptArgs": "",
                    "isRepoScript": False,
                    "name": "AScriptName"
                }
            }
        }
    }
    b.launch_client(s, qs=launch_script)

