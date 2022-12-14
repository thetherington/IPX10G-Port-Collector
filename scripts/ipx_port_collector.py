import copy
import json

import requests


class IPXPortCollector:
    def __init__(self, **kwargs):

        self.address = None

        self.input_rate = {
            "id": "32.<replace>@i",
            "type": "integer",
            "name": "l_input_rate",
        }
        self.output_rate = {
            "id": "33.<replace>@i",
            "type": "integer",
            "name": "l_output_rate",
        }
        self.port_label = {"id": "306.<replace>@s", "type": "string", "name": "s_label"}
        self.port_status = {
            "id": "252.<replace>@i",
            "type": "integer",
            "name": "s_operation_status",
        }
        self.port_name = {"id": "303.<replace>@s", "type": "string", "name": "s_name"}

        self.parameters = []

        self.port_store = {}

        self.fetch = self.fetch_ipx

        for key, value in kwargs.items():

            if "address" in key and value:
                self.address = value

            if "ports" in key and value:

                port_list = []
                for port in value:

                    if isinstance(port, str) and "-" in port:

                        start, stop = port.split("-")
                        port_list.extend(list(range(int(start), int(stop) + 1)))

                    else:
                        port_list.append(port)

                port_list = list(set(port_list))

                for port in port_list:

                    for template in [
                        self.input_rate,
                        self.output_rate,
                        self.port_label,
                        self.port_status,
                        self.port_name,
                    ]:

                        template_copy = copy.deepcopy(template)
                        template_copy["id"] = template_copy["id"].replace(
                            "<replace>", str(port - 1)
                        )

                        self.parameters.append(template_copy)

    def fetch_ipx(self, parameters):

        try:

            with requests.Session() as session:

                ## get the session ID from accessing the login.php site
                resp = session.get(
                    "http://%s/login.php" % self.address,
                    verify=False,
                    timeout=30.0,
                )

                session_id = resp.headers["Set-Cookie"].split(";")[0]

                payload = {
                    "jsonrpc": "2.0",
                    "method": "get",
                    "params": {"parameters": parameters},
                    "id": 1,
                }

                url = "http://%s/cgi-bin/cfgjsonrpc" % (self.address)

                headers = {
                    "content_type": "application/json",
                    "Cookie": session_id + "; webeasy-loggedin=true",
                }

                response = session.post(
                    url,
                    headers=headers,
                    data=json.dumps(payload),
                    verify=False,
                    timeout=30.0,
                )

                return json.loads(response.text)

        except Exception as error:
            print(error)
            return error

    @property
    def collect(self):

        results = self.fetch(self.parameters)

        ports = {}

        for result in results["result"]["parameters"]:

            try:

                # seperate "240.1@i" to "1@i"
                _id = result["id"].split(".")[1]

                # split the instance and type notation, then convert the
                # instance back to base 1 for port number
                _instance = _id.split("@")[0]
                _instance = int(_instance) + 1

                key = result["name"]

                if "operation_status" in key:

                    lookup = {0: "UP", 1: "DOWN"}
                    result["value"] = lookup[result["value"]]

                if "rate" in key:
                    result["value"] = result["value"] * 1000

                # create port key and object if doesn't exist, otherwise update existing key/object
                if _instance not in ports.keys():

                    ports.update(
                        {
                            _instance: {
                                key: result["value"],
                                "as_id": [result["id"]],
                                "i_port": _instance,
                            }
                        }
                    )

                else:

                    ports[_instance].update({key: result["value"]})
                    ports[_instance]["as_id"].append(result["id"])

            except Exception as error:
                print(error)

        return ports


def main():

    params = {"address": "127.83.151.223", "ports": ["1-64"]}

    ipx = IPXPortCollector(**params)

    for _, items in ipx.collect.items():
        print(json.dumps(items, indent=1))


if __name__ == "__main__":
    main()
