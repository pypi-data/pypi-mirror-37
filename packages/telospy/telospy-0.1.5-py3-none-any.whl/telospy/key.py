import base58
import ecdsa
import re
import os
import time
import struct
from binascii import hexlify, unhexlify
import hashlib


def sha256(data):
    ''' '''
    return hashlib.sha256(data).hexdigest()


def ripemd160(data):
    ''' '''
    #h = hashlib.new('ripemd160')
    h = hashlib.new('rmd160')
    h.update(data)
    return h.hexdigest()


def int_to_hex(i):
    return '{:02x}'.format(i)


def hex_to_int(i):
    return int(i, 16)


def str_to_hex(c):
    hex_data = hexlify(bytearray(c, 'ascii')).decode()
    return int(hex_data, 16)


class Key(object):
    def __init__(self, private_str=''):
        if private_str:
            private_key, format, key_type = self._parse_key(private_str)
            self._sk = ecdsa.SigningKey.from_string(unhexlify(private_key), curve=ecdsa.SECP256k1)
        else:
            prng = self._create_entropy()
            self._sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1, entropy=prng)
        self._vk = self._sk.get_verifying_key()

    def __str__(self):
        return self.to_public()

    def _parse_key(self, private_str):
        match = re.search('^PVT_([A-Za-z0-9]+)_([A-Za-z0-9]+)$', private_str)
        if not match:
            # legacy WIF - format
            version_key = self._check_decode(private_str, 'sha256x2')
            # ensure first 2 chars == 0x80
            version = int(version_key[0:2], 16)
            if not version == 0x80:
                raise ValueError('Expected version 0x80, instead got {0}', version)
            private_key = version_key[2:]
            key_type = 'K1'
            format = 'WIF'
        else:
            key_type, key_string = match.groups()
            private_key = self._check_decode(key_string, key_type)
            format = 'PVT'
        return (private_key, format, key_type)

    def _create_entropy(self):
        ba = bytearray(os.urandom(32))
        seed = sha256(ba)
        return ecdsa.util.PRNG(seed)

    def _check_encode(self, key_buffer, key_type=None):
        if isinstance(key_buffer, bytes):
            key_buffer = key_buffer.decode()
        check = key_buffer
        if key_type == 'sha256x2':
            first_sha = sha256(unhexlify(check))
            chksum = sha256(unhexlify(first_sha))[:8]
        else:
            if key_type:
                check += hexlify(bytearray(key_type, 'utf-8')).decode()
            chksum = ripemd160(unhexlify(check))[:8]
        return base58.b58encode(unhexlify(key_buffer + chksum))

    def _check_decode(self, key_string, key_type=None):
        buffer = hexlify(base58.b58decode(key_string)).decode()
        chksum = buffer[-8:]
        key = buffer[:-8]
        if key_type == 'sha256x2':
            # legacy
            first_sha = sha256(unhexlify(key))
            newChk = sha256(unhexlify(first_sha))[:8]
        else:
            check = key
            if key_type:
                check += hexlify(bytearray(key_type, 'utf-8')).decode()
            newChk = ripemd160(unhexlify(check))[:8]
        # print('newChk: '+newChk)
        if chksum != newChk:
            raise ValueError('checksums do not match: {0} != {1}'.format(chksum, newChk))
        return key

    def _recovery_pubkey_param(self, digest, signature):
        ''' Use to derive a number that will allow for the easy recovery
            of the public key from the signature'''
        for i in range(0, 4):
            p = self._recover_key(digest, signature, i)
            if (p.to_string() == self._vk.to_string()):
                return i

    def _compress_pubkey(self):
        order = self._sk.curve.generator.order()
        p = self._vk.pubkey.point
        x_str = ecdsa.util.number_to_string(p.x(), order)
        hex_data = bytearray(chr(2 + (p.y() & 1)), 'utf-8')
        compressed = hexlify(hex_data + x_str).decode()
        return compressed

    def to_public(self):
        cmp = self._compress_pubkey()
        return 'TLOS' + self._check_encode(cmp).decode()

    def to_wif(self):
        pri_key = '80' + hexlify(self._sk.to_string()).decode()
        return self._check_encode(pri_key, 'sha256x2').decode()