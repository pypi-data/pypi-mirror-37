# -*- coding: utf-8 -*-

"""to make api api_doc as monitor config"""
from datetime import datetime, date
from monitor_register.api_doc.api_doc import APIDoc
from monitor_register.util.file_util import read_json


def save_doc_as_monitor_config(input_json_file: str, output_file_path: str, host: str, app_id: int,
                            time_interval: int, version: int = 1,
                            created_at: date = datetime.now()):
    """save api_doc as monitor config json

    :param input_json_file: input json path
    :param output_file_path: save path
    :param host: your server host
    :param app_id: app id which could get in api.gagogroup.cn
    :param time_interval: the frequency of sending requests
    :param version: api version
    :param created_at: created time
    :return: None
    """

    json_contents = read_json(input_json_file)
    api_doc = APIDoc(json_contents)
    api_doc.save_doc_as_monitor_config(output_file_path, host, app_id, time_interval, version, created_at)


def register_to_monitor_server(input_json_file: str, monitor_host: str, monitor_token: str, api_host: str, app_id: int,
                               time_interval: int, version: int = 1,
                               created_at: date = datetime.now()):
    """register api api_doc to monitor server

    :param input_json_file: input json path
    :param monitor_host: monitor server protocol://host_or_ip
    :param monitor_token: monitor token which could get in api.gagogroup.cn
    :param api_host: your server host
    :param app_id: app id which could get in api.gagogroup.cn
    :param time_interval: the frequency of sending requests
    :param version: api version
    :param created_at: created time
    :return: result
    """

    json_contents = read_json(input_json_file)
    api_doc = APIDoc(json_contents)
    res_json = api_doc.register_to_monitor_server(monitor_host, monitor_token, api_host, app_id, time_interval, version, created_at)
    return res_json
