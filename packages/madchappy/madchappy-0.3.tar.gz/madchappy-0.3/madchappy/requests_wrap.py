# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
"""
Various helpers to query web services
"""
import requests


def get_data(url, verify=False):
    """

    :param url: target url to GET
    :param verify: Boolean to check or not TLS certificates
    :return: returns JSON response object
    """
    return requests.get(url=url, verify=verify).json()


def post_data(url, verify=False):
    """

    :param url: target url to POST to
    :param verify: Boolean to check or not TLS certificates
    :return: returns JSON response object
    """
    return requests.post(url=url, verify=verify).json()
