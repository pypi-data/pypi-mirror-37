# -*- coding: utf-8 -*-

"""api_doc class"""
import json
from datetime import date, datetime

import requests

from monitor_register.util.file_util import write_file


class APIDoc(object):
    """to save and process api api_doc"""

    def __init__(self, obj):
        self.doc = obj

    def get_monitor_config_object(self, host: str, app_id: int, time_interval: int, version: int = 1,
                                  created_at: date = datetime.now()):
        """get monitor config object"""

        return {
            'appId': app_id,
            'version': version,
            'createdAt': created_at.isoformat(),
            'timeInterval': time_interval,
            'host': host,
            'api': self.doc
        }

    def doc_to_monitor_config(self, host: str, app_id: int, time_interval: int, version: int = 1,
                              created_at: date = datetime.now()) -> str:
        """generate monitor config json

        :param host: your server host
        :param app_id: app id which could get in api.gagogroup.cn
        :param time_interval: the frequency of sending requests
        :param version: api version
        :param created_at: created time
        :return: json
        """

        final_json = json.dumps(self.get_monitor_config_object(host, app_id, time_interval, version, created_at),
                                ensure_ascii=False)
        return final_json

    def save_doc_as_monitor_config(self, output_file_path: str, host: str, app_id: int, time_interval: int,
                                   version: int = 1,
                                   created_at: date = datetime.now()) -> str:
        """save api_doc as monitor config json

        :param output_file_path: save path
        :param host: your server host
        :param app_id: app id which could get in api.gagogroup.cn
        :param time_interval: the frequency of sending requests
        :param version: api version
        :param created_at: created time
        :return: json
        """

        final_json = json.dumps(self.get_monitor_config_object(host, app_id, time_interval, version, created_at),
                                ensure_ascii=False)
        write_file(output_file_path, final_json)

    def register_to_monitor_server(self, monitor_host: str, monitor_token: str, api_host: str, app_id: int,
                                   time_interval: int, version: int = 1,
                                   created_at: date = datetime.now()):
        """register api api_doc to monitor server

        :param monitor_host: monitor server protocol://host_or_ip
        :param monitor_token: monitor token which could get in api.gagogroup.cn
        :param api_host: your server host
        :param app_id: app id which could get in api.gagogroup.cn
        :param time_interval: the frequency of sending requests
        :param version: api version
        :param created_at: created time
        :return: result
        """

        session = requests.Session()
        headers = {'token': monitor_token}
        session.headers.update(headers)
        monitor_config = self.get_monitor_config_object(api_host, app_id, time_interval, version, created_at)
        req = session.post(monitor_host + '/api/v1/monitor/config', json=monitor_config)
        res_json = req.json()
        session.close()
        return res_json
