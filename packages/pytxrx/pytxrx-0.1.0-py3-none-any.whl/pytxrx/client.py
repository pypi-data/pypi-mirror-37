#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# client.py (0.1.0)
#
# Developed in 2018 by Travis Kessler <travis.j.kessler@gmail.com>
#

from socket import socket, AF_INET, SOCK_DGRAM
from pytxrx import send_message


class Client:

    def __init__(self, ip, r_port, t_port):
        '''
        Client object: sends messages to servers

        Args:
            ip (str): IP address of the Client
            r_port (int): port to receive acknowledgements on
            t_port (int): port to send messages on
        '''

        self.__ip = ip
        self.__r_port = r_port
        self.__t_port = t_port
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind((self.__ip, self.__r_port))
        self.socket.setblocking(False)

    def send_message(self, data):
        '''
        Sends a message

        Args:
            data (str or bytes): data to send
        '''

        send_message(self.socket, self.__ip, self.__t_port, data)
