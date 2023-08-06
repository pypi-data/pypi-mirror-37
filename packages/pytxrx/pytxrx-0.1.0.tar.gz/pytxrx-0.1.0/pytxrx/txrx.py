#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# txrx.py (0.1.0)
#
# Developed in 2018 by Travis Kessler <travis.j.kessler@gmail.com>
#

# Stdlib imports
from threading import Event, Timer

# PyTxRx imports
from pytxrx import MessageFrame, TransferMessage, ReceiveMessage

# Constants
TIMEOUT = 0.5
WINDOW_SIZE = 10
MSG_HEADER_LEN = 6
MSG_TOTAL_LEN = 256
ACK_MESSAGE = 'ACK'
ACK_LENGTH = len(ACK_MESSAGE) + MSG_HEADER_LEN


def socket_send(socket, ip, port, message):
    '''
    Sends a message

    Args:
        socket (socket.socket()): bound socket
        ip (str): IP address to send to
        port (int): port to use when sending
        message (bytes): message to send
    '''

    socket.sendto(message, (ip, port))


def socket_receive(socket, msg_len):
    '''
    Receives a message

    Args:
        socket (socket.socket()): bound socket
        msg_len (int): length of message to receive

    Returns:
        bytes: message received using socket
        None: if an error occurred during receiving
    '''

    try:
        return socket.recv(msg_len)
    except:
        return None


def send_message(socket, ip, t_port, data):
    '''
    Sends a message using TCP static windowing

    Args:
        socket (socket.socket()): bound socket
        ip (str): IP address to be sent to
        t_port (int): port used for transfer
        data (str or bytes): message to send
    '''

    transfer_message = TransferMessage(data)

    acknowledgement = MessageFrame()
    index = 0

    frames = [MessageFrame(index, transfer_message.preamble)]
    frames += transfer_message.frames

    window_start = 0

    timeout = Event()
    timer = Timer(TIMEOUT, lambda t: t.set(), [timeout])
    timer.start()

    while window_start < len(frames):

        # Timeout has occurred
        if timeout.isSet():

            timeout.clear()
            timer.cancel()
            timer = Timer(TIMEOUT, lambda t: t.set(), [timeout])
            timer.start()

            for frame in range(window_start, index):
                socket_send(socket, ip, t_port, frames[frame].pack())

        # Message not completely sent, send next frame in window
        elif index < len(frames) and index < (window_start + WINDOW_SIZE):

            frames[index].index_num = index
            socket_send(socket, ip, t_port, frames[index].pack())
            index += 1

        # Message and/or window sent
        else:

            received_ack = socket_receive(socket, ACK_LENGTH)
            if received_ack is None:
                continue

            acknowledgement.unpack(received_ack)
            if not acknowledgement.correct_cs:
                continue

            else:
                if acknowledgement.index_num == 0:
                    window_start = 0
                else:
                    window_start = acknowledgement.index_num + 1

                if window_start == index:
                    timer.cancel()
                else:
                    timer.cancel()
                    timer = Timer(TIMEOUT, lambda t: t.set(), [timeout])
                    timer.start()


def receive_message(socket, ip, t_port):
    '''
    Receives a message over TCP

    Args:
        socket (socket.socket()): bound socket
        ip: IP address to send acknowledgements to
        t_port: port to send acknowledgements through

    Returns:
        ReceiveMessage: message received from transfer
    '''

    frame = MessageFrame()
    message = None
    index = 0
    acknowledgement = MessageFrame(index, ACK_MESSAGE)

    while True:

        received_frame = socket_receive(socket, MSG_TOTAL_LEN)
        if received_frame is None:
            continue

        frame.unpack(received_frame)
        if frame.index_num == index and frame.correct_cs:

            if message is not None:
                message.add_frame(frame)
            else:
                message = ReceiveMessage(frame.data)

            acknowledgement = MessageFrame(index, ACK_MESSAGE)
            index += 1

        socket_send(socket, ip, t_port, acknowledgement.pack())

        if message is None:
            continue

        if message.is_complete and message is not None:
            break

    return message
