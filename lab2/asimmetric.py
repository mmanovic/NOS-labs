import os
from Crypto import Random
from base64 import b64encode, b64decode
from Crypto.PublicKey import ElGamal
from Crypto.PublicKey import RSA
from Crypto import Random
import tkinter.filedialog
from util import *


class ASimCrypt:
    def __init__(self):
        self.public_key_path = 'files/asim_public_key.txt'
        self.private_key_path = 'files/asim_private_key.txt'

    def generate(self, keySize, algorithm):
        self.keysize = keySize.get()
        random_generator = Random.new().read
        if algorithm.get() == 'RSA':
            kljuc = RSA.generate(keySize.get(), random_generator)  # generiram par kljuceva
            modulus = kljuc.n
            public_exp = kljuc.e
            private_exp = kljuc.d
        else:
            kljuc = ElGamal.generate(keySize.get(), random_generator)  # generiram par kljuceva
            modulus = kljuc.p
            public_exp = kljuc.y
            private_exp = kljuc.x
            generator = kljuc.g

        # Zapis javnog:
        file = open(self.public_key_path, 'w')
        file.write('---BEGIN OS2 CRYPTO DATA---\n')
        file.write('Description:\n    Public key\n\n')
        file.write('Method:\n    ' + algorithm.get() + '\n\n')
        file.write('File name:\n    ')
        file.write(self.public_key_path)
        file.write('\n\nKey length:\n    ' + (str(hex(self.keysize))).replace('0x', ''))
        file.write('\n\nModulus:\n    ')
        write_to_file(file, str(hex(modulus)).replace('0x', '').upper())
        file.write('\n\nPublic exponent:\n    ')
        write_to_file(file, str(hex(public_exp)).replace('0x', '').upper())
        if algorithm.get() != 'RSA':
            file.write('\n\nGenerator:\n    ')
            write_to_file(file, str(hex(generator)).replace('0x', '').upper())
        file.write('\n\n---END OS2 CRYPTO DATA---')

        # Zapis privatnog
        file = open(self.private_key_path, 'w')
        file.write('---BEGIN OS2 CRYPTO DATA---\n')
        file.write('Description:\n    Private key\n\n')
        file.write('Method:\n    ' + algorithm.get() + '\n\n')
        file.write('File name:\n    ')
        file.write(self.private_key_path)
        file.write('\n\nKey length:\n    ' + (str(hex(keySize.get()))).replace('0x', ''))
        file.write('\n\nModulus:\n    ')
        write_to_file(file, str(hex(modulus)).replace('0x', '').upper())
        file.write('\n\nPrivate exponent:\n    ')
        write_to_file(file, str(hex(private_exp)).replace('0x', '').upper())
        if algorithm.get() != 'RSA':
            file.write('\n\nGenerator:\n    ')
            write_to_file(file, str(hex(generator)).replace('0x', '').upper())
        file.write('\n\n---END OS2 CRYPTO DATA---')

    def choose_public(self, key_path):
        choosen = tkinter.filedialog.askopenfilename(initialdir='files')
        self.public_key_path = choosen
        key_path.set(self.public_key_path)

    def choose_private(self, key_path):
        choosen = tkinter.filedialog.askopenfilename(initialdir='files')
        self.private_key_path = choosen
        key_path.set(self.private_key_path)

    def ByteToHex(self, byteStr):
        return ''.join(["%02X" % x for x in byteStr]).strip()

    def HexToByte(self, hexStr):
        return bytes.fromhex(hexStr)
