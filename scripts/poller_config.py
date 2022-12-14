import json
from insite_plugin import InsitePlugin
from ipx_port_collector import IPXPortCollector


class Plugin(InsitePlugin):
    def can_group(self):
        return False

    def fetch(self, hosts):

        host = hosts[-1]

        try:

            self.ipx

        except Exception:

            params = {"address": host, "ports": ["1-64"]}

            self.ipx = IPXPortCollector(**params)

        documents = []

        for _, params in self.ipx.collect.items():

            document = {"fields": params, "host": host, "name": "ipx"}

            documents.append(document)

        return json.dumps(documents)
