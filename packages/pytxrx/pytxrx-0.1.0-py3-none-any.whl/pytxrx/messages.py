#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# messages.py (0.1.0)
#
# Developed in 2018 by Travis Kessler <travis.j.kessler@gmail.com>
#

# Stdlib imports
from copy import deepcopy
from math import ceil
from struct import pack, unpack

# Constants
MSG_TOTAL_LEN = 256
MSG_HEADER_LEN = 6
MSG_BODY_LEN = MSG_TOTAL_LEN - MSG_HEADER_LEN


class MessageFrame:

    def __init__(self, index_num=None, data=''):
        '''
        MessageFrame object: encapsulates data for a message frame to be sent

        Args:
            index_num (int): optional frame index for frame ordering
            data (str or bytes): data to be housed by the MessageFrame
        '''

        if index_num is None:
            index_num = 99999999
        self.__index_num = index_num
        if type(data) is str:
            data = data.encode()
        if type(data) is not bytes:
            raise ValueError('Data must be supplied in String or Bytes!')
        self.data = data
        self.__cs = self.__gen_cs()

    def pack(self):
        '''
        Uses struct.pack() to pack the MessageFrame's index number, checksum,
        and data; packs in (unsigned int, unsigned short, char[]) format

        Returns:
            bytes value of packed information
        '''

        return pack(
            'IH{}s'.format(len(self.data)),
            self.__index_num,
            self.__cs,
            self.data
        )

    def unpack(self, message):
        '''
        Uses struct.unpack() to unpack a bytes value in (unsigned int,
        unsigned short, char[]) format to the MessageFrame's index number,
        checksum, and data respectively

        Args:
            message (bytes): a bytes value packed as (unsigned int, unsigned
                             short, char[])
        '''

        message = unpack(
            'IH{}s'.format(len(message) - MSG_HEADER_LEN),
            message
        )
        self.__index_num, self.__cs, self.data = message[0:3]

    def __gen_cs(self):
        '''
        Private method: generates a checksum for the MessageFrame, derived
        from the MessageFrame's index number and data
        '''

        message = pack('I', self.__index_num) + self.data
        if len(message) % 2 is not 0:
            message += b'\0'
        num_h = ''
        for _ in range(int(len(message)/2)):
            num_h += 'H'
        vals = unpack(num_h, message)
        cs = vals[0]
        for val in vals[1:]:
            cs = self.__cs_bit_add(cs, val)
        return ~cs & 0xffff

    @staticmethod
    def __cs_bit_add(l, r):
        '''
        Private, static method: used by self.__gen_cs() to bitwise add the
        next unsigned short value to the checksum

        Args:
            l (unsigned short): current checksum value
            r (unsigned short): value to add to the current checksum value

        Returns:
            unsigned short: result of bitwise add of l and r
        '''

        r += l
        return (r & 0xffff) + (r >> 16)

    @property
    def correct_cs(self):
        '''
        Property: determines whether checksum obtained with self.unpack()
        should match the index number obtained with self.unpack() (used to
        determine correct frame ordering during transfer)

        Returns:
            bool: True if correct frame order, False if not correct frame order
        '''

        return self.__cs == self.__gen_cs()

    @property
    def index_num(self):
        '''
        Property: index number of the MessageFrame

        Returns:
            int: MessageFrame's index number
        '''

        return self.__index_num

    @index_num.setter
    def index_num(self, index_num):
        '''
        Property setter: sets the index number for the frame, generates a new
        checksum for the frame

        Args:
            index_num (int): new index number for the frame
        '''

        self.__index_num = index_num
        self.__cs = self.__gen_cs()


class TransferMessage:

    def __init__(self, data):
        '''
        TransferMessage object: compiles the data to be sent into MessageFrame
        objects

        Args:
            data (str or bytes): data to be sent
        '''

        self.__message_frames = []
        self.__id = 0

        num_frames = int(ceil(len(data) / float(MSG_BODY_LEN)))
        for i in range(num_frames):

            frame_start = MSG_BODY_LEN * i
            frame_end = MSG_BODY_LEN + frame_start

            if frame_end < len(data):
                self.__add_frame(data[frame_start:frame_end])
            else:
                self.__add_frame(data[frame_start:])

    def __add_frame(self, data):
        '''
        Private method: used during TransferMessage initialization to append a
        MessageFrame object to the current list of frames

        Args:
            data (str or bytes): portion of data passed during initialization
                                 to be packed into an individual MessageFrame
        '''

        self.__message_frames.append(MessageFrame(self.__id, data))
        self.__id += 1

    @property
    def frames(self):
        '''
        Property: list of current MessageFrames for the TransferMessage

        Returns:
            list: list of MessageFrame objects
        '''

        return self.__message_frames

    @property
    def preamble(self):
        '''
        Property: preamble of the TransferMessage, i.e. the number of frames
        the receiver should expect

        Returns:
            bytes value packed with struct.pack(), containing (unsigned int)
        '''

        return pack('I', len(self.__message_frames))


class ReceiveMessage:

    def __init__(self, preamble):
        '''
        ReceiveMessage object: used to compile MessageFrames received during a
        transfer

        Args:
            preamble (bytes): packed bytes message in (unsigned int) format,
                              containing the number of MessageFrame objects to
                              expect for a transfer
        '''

        self.__message_frames = []
        self.__num_frames_expected = unpack('I', preamble)[0]

    def add_frame(self, frame):
        '''
        Appends a received MessageFrame object to the ReceiveMessages list of
        frames

        Args:
            frame (MessageFrame): MessageFrame object to add
        '''

        self.__message_frames.append(deepcopy(frame))

    @property
    def is_complete(self):
        '''
        Property: determines whether the transfer is complete, i.e. the number
        of MessageFrame objects housed by ReceiveMessage is equal to the
        number expected

        Returns:
            bool: True if the number of frames == number expected, False
                  otherwise
        '''

        return len(self.__message_frames) == self.__num_frames_expected

    @property
    def data(self):
        '''
        Property: all bytes data housed in the ReceiveMessage

        Returns:
            bytes: ordered bytes data of all MessageFrame objects in
                   ReceiveMessage
        '''

        return b''.join(f.data for f in self.__message_frames)
