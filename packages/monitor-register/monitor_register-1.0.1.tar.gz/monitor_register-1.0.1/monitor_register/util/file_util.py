# -*- coding: utf-8 -*-

"""file util"""
import json
import os


def read_json(file_path: str) -> str:
    """read json

    :param file_path: path
    :return:
    """
    with open(file_path) as fd:
        json_data = json.load(fd)
    return json_data


def write_file(file_path: str, file_content: str):
    """write file

    :param file_path: path
    :param file_content: content
    :return:
    """
    with open(file_path, 'w') as out_file:
        out_file.write(file_content)


def remove_file(file_path: str):
    """remove file

    :param file_path: path
    :return:
    """
    if os.path.isfile(file_path):
        os.remove(file_path)
    else:
        raise ("Error: %s file not found" % file_path)
