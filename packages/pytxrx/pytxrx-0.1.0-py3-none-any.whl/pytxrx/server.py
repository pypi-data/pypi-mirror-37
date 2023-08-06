#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# server.py (0.1.0)
#
# Developed in 2018 by Travis Kessler <travis.j.kessler@gmail.com>
#

# Stdlib imports
from socket import socket, AF_INET, SOCK_DGRAM

# PyTxRx imports
from pytxrx import receive_message


class Server:

    def __init__(self, ip, r_port, t_port):
        '''
        Server object: receives messages from clients

        Args:
            ip (str): IP address of the Server
            r_port (int): port to receive messages on
            t_port (int): port to send acknowledgements on
        '''

        self.__ip = ip
        self.__r_port = r_port
        self.__t_port = t_port
        self.__socket = socket(AF_INET, SOCK_DGRAM)
        self.__socket.bind((self.__ip, self.__r_port))

    def receive_message(self):
        '''
        Receives a message

        Returns:
            ReceiveMessage: message received from a client
        '''

        return receive_message(self.__socket, self.__ip, self.__t_port)
