# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 20:07:11 2018

@author: Misha
"""

import socket
import sys

from settings import REC_FILE, UPLOAD_URLS, UPLOAD_PORT

try:
    import tkinter.messagebox as messagebox
except ImportError:
    import tkMessageBox as messagebox

# solution for issue #16
if sys.version_info[0] == 2:
    def encoder(string):
        return string.encode('ascii')
else:
    def encoder(string):
        return bytes(string, 'ascii')



class Uploader(object):

    def __init__(self, handler=None):
        self.handler = handler
        self.filename = REC_FILE
        self.lines = None
        self.socket = None
        self.has_connection = False

    def establish_connection(self):
        for url in UPLOAD_URLS:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.settimeout(30)  # it's slow...
                self.socket.connect((url, int(UPLOAD_PORT)))
                self.has_connection = True

            except Exception as exc:
                # Welp, that one didn't work... keep going!
                # TODO: implement GUI message here
                pass

        return self.has_connection

    def send_data(self):
        if not self.has_connection:
            raise ValueError("Can't upload data with no connection!")

        with open(self.filename, 'r') as infile:
            self.lines = infile.readlines()

        text = ''.join(self.lines)
        encoded = encoder(text)
        # TODO: GUI message
        self.socket.sendall(encoded)

        with open(self.filename, 'w') as handle:
            handle.write('')

    def upload(self):
        self.establish_connection()
        self.send_data()
