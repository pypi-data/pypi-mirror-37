#!/usr/bin/env python3
# coding=utf-8
# author: @netmanchris
# -*- coding: utf-8 -*-
"""
This module contains functions for authenticating to the Attelani Brid Air Purifier Device
API.

"""


class BridAuth:
    """
    Object to hold the authentication data for the Brid API
    Note currently, the Brid API requires no authentication. Auth object is created
    to allow for caching of IP address of Brid Device and for future enhancements.
    :return An object of class AwairAuth to be passed into other functions to
    pass the authentication credentials
    """

    def __init__(self, ipaddress):
        """
        This class acts as the auth object for the Awair API. The token is available from the
        Awair developer website.
        :param token: str object which contains the
        """

        self.ipaddress = ipaddress
        self.headers = {
            'Accept': 'application/json', 'Content-Type':
                'application/json', 'Accept-encoding': 'application/json'}
