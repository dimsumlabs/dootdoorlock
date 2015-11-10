import socket
import sys

__all__ = ['door', 'rfid_auth']

SOCK_PATH = '/tmp/doord'


def _sock():
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        s.connect(SOCK_PATH)
    except socket.error as e:
        if e.errno == 2:
            sys.stderr.write('Socket not found, is doord running?')
            s.close()
        else:
            raise
    else:
        return s


def _wrap_send(command):
    s = _sock()
    if s is None:
        return

    try:
        s.send(command)
    finally:
        s.close()


class door(object):

    @staticmethod
    def open():
        _wrap_send(b'OPEN')

    @staticmethod
    def close():
        _wrap_send(b'CLOSE')
