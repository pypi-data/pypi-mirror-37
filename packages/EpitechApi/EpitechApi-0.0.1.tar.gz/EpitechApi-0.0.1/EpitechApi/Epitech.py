#!/bin/env python3
import requests
import json
import re


class EpitechApi(object):
    def __init__(self, auto_login):
        """
        :param auto_login: your epitech auto login url
                you can get yours here: https://intra.epitech.eu/admin/autolog
        """
        response = requests.get(auto_login)
        if response.status_code != 200:
            raise ConnectionRefusedError
        self.auto_login = auto_login
        if auto_login[-1] != '/':
            self.auto_login += "/"

    """
        Here evrey method are juste doing get requests on evrey possible urls
        no arguments are need because you can get only your information
    """
    def get_messages(self):
        response = requests.get(self.auto_login + 'user/notification/message', params={'format': 'json'})
        if response.status_code != 200:
            raise ConnectionRefusedError
        return json.loads(response.content)

    def get_alerts(self):
        response = requests.get(self.auto_login + 'user/notification/alert', params={'format': 'json'})
        if response.status_code != 200:
            raise ConnectionRefusedError
        return json.loads(response.content)

    def get_coming(self):
        response = requests.get(self.auto_login + 'user/notification/coming', params={'format': 'json'})
        if response.status_code != 200:
            raise ConnectionRefusedError
        return json.loads(response.content)

    def get_generals_information(self):
        response = requests.get(self.auto_login + 'user/', params={'format': 'json'})
        if response.status_code != 200:
            raise ConnectionRefusedError
        return json.loads(response.content)

    def get_grades(self):
        response = requests.get(self.auto_login + 'user/#!/notes')
        if response.status_code != 200:
            raise ConnectionRefusedError
        to_comp = response.content.decode()
        to_comp = to_comp.replace('\n', '')
        to_comp = to_comp.replace('\r', '')
        to_comp = to_comp.replace('\t', '')
        res = re.search(r'.+modules:(\[.+\]),notes: \[{.+', to_comp)
        res = json.loads(res.group(1))
        return res

    def get_notes(self):
        response = requests.get(self.auto_login + 'user/#!/notes')
        if response.status_code != 200:
            raise ConnectionRefusedError
        to_comp = response.content.decode()
        to_comp = to_comp.replace('\n', '')
        to_comp = to_comp.replace('\r', '')
        to_comp = to_comp.replace('\t', '')
        res = re.search('.+,notes: (\[.+\])}\);.+{flags:.+', to_comp)
        res = json.loads(res.group(1))
        return res

    def get_netsoul(self):
        """
        TODO: look at the html and get information of it.
        :return:
        """
        pass
