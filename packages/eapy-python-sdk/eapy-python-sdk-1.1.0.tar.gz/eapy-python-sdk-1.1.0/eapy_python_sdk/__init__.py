import requests

class Eapy:

    def __init__(self, authentication_token=None,
                 environment="http://api.eapy.eu",
                 prefix="/eapy/api/2.0", timeout=1000):
        self.endpoint = environment + prefix
        self.timeout = timeout
        self.authentication_token = authentication_token
        requests.get(self.endpoint, timeout=timeout)

    def connect(self, username="", pwd=""):
        request = requests.post(self.endpoint + "/login", json={"email": username, "password": pwd},
                                timeout=self.timeout)

        if request.status_code != 200:
            return {"status_code": request.status_code, "errors": request.reason,
                    "exception": request.raise_for_status()}

        response = {"status_code": request.json()['meta']['code']}
        if response["status_code"] != 200:
            response["errors"] = request.json()['response']['errors']
            response["exception"] = Exception(request.json()['response']['errors'])

            raise Exception(str(response))
        else:
            self.authentication_token = request.json()['response']['user']['authentication_token']

        return response

    def _build_reponse(self, request):

        response = {"status_code": request.status_code}

        if request.status_code != 200:
            response["errors"] = request.reason
            try:
                request.raise_for_status()
            except Exception as e:
                response["exception"] = e

            response["message"] = request.content
        else:
            response["results"] = request.json()

        return response

    def empty_object_class(self, repository, object_class):
        url = self.endpoint + "/repositories/<rep_id>/objectclasses/<class_name>/empty"
        url = url.replace("<rep_id>", str(repository))
        url = url.replace("<class_name>", object_class)
        header = {
            "Authentication-Token": self.authentication_token
        }

        request = requests.delete(url, headers=header, timeout=self.timeout)

        return self._build_reponse(request)

    def remove_object(self, repository, object_class, object_key):
        url = self.endpoint + "/repositories/<rep_id>/objectclasses/<class_name>/objects/key/<object_key>"
        url = url.replace("<rep_id>", str(repository))
        url = url.replace("<class_name>", object_class)
        url = url.replace("<object_key>", object_key)
        header = {
            "Authentication-Token": self.authentication_token
        }

        request = requests.delete(url, headers=header, timeout=self.timeout)

        return self._build_reponse(request)

    def add_edit_object(self, repository, object_class, object):
        url = self.endpoint+"/repositories/<rep_id>/objectclasses/<class_name>"
        url = url.replace("<rep_id>", str(repository))
        url = url.replace("<class_name>", object_class)
        header = {
            "Authentication-Token": self.authentication_token
        }
        payload = {
            "object":object
        }
        request = requests.post(url, json=payload, headers=header, timeout=self.timeout)

        return self._build_reponse(request)

    def business_rule(self, repository, rule_type, rule_name, params):
        url = self.endpoint + "/repositories/" + str(repository) + "/business-rules/" + rule_type + "/" + rule_name
        header = {"Authentication-Token": self.authentication_token}
        payload = {"params": params}
        request = requests.post(url, json=payload, headers=header, timeout=self.timeout)

        response = {"status_code": request.status_code}

        if request.status_code != 200:
            response["errors"] = request.reason
            response["exception"] = request.raise_for_status()
        else:
            response["results"] = request.json()["results"]
            response["input_params"] = request.json()["input_params"]

        return response

    def data_view(self, repository, view_type, view_name, params):
        url = self.endpoint + "/repositories/" + str(repository) + "/search/" + view_type + "/" + view_name
        header = {"Authentication-Token": self.authentication_token}
        payload = {"params": params}
        request = requests.post(url, json=payload, headers=header, timeout=self.timeout)

        response = {"status_code": request.status_code}

        if request.status_code != 200:
            response["errors"] = request.reason
            response["exception"] = request.raise_for_status()
        else:
            response["results"] = request.json()

        return response
