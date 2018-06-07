import os
from Crypto.Cipher import AES
from Crypto.Cipher import DES3
from Crypto.PublicKey import ElGamal
from Crypto.PublicKey import RSA
from Crypto.Util.number import GCD
from Crypto.Random import random
import hashlib
from base64 import b64encode, b64decode
import tkinter.messagebox
import tkinter.filedialog
from util import *


class Signature:
    def __init__(self):
        self.input_path = 'files/ulaz.txt'
        self.private_key_path = 'files/asim_private_key.txt'
        self.signature_path = 'files/signature.txt'
        self.public_key_path = 'files/asim_public_key.txt'

    def generate(self, hash_function):
        data = get_data(self.input_path, 'Data')
        modulus = int(int(get_data(self.private_key_path, 'Modulus'), 16))
        private_exp = int(int(get_data(self.private_key_path, 'Private exponent'), 16))
        public_exp = int(int(get_data(self.public_key_path, 'Public exponent').strip(), 16))
        private_key_size = get_data(self.private_key_path, 'Key length')
        asimmetric_alg = get_data(self.private_key_path, 'Method')
        m = hashlib.new(hash_function.get())
        m.update(data.encode(encoding='utf-8'))
        hash = m.digest()
        if (asimmetric_alg == 'RSA'):
            RSAEncryptor = RSA.construct((modulus, public_exp, private_exp))
            signature = RSAEncryptor.sign(hash, '')[0]
            self.signature_second_part = ''
        else:
            generator = int(int(get_data(self.private_key_path, 'Generator'), 16))
            ElGamalEncryptor = ElGamal.construct((modulus, generator, public_exp, private_exp))
            while 1:
                k = random.StrongRandom().randint(1, int(modulus - 1))
                if GCD(k, int(modulus - 1)) == 1: break
            signature = ElGamalEncryptor.sign(hash, int(k))
            k = signature[1]
            signature = signature[0]
            self.signature = signature

        data = b64encode(data.encode())
        signature = hex(signature)
        # zapisivanje
        file = open(self.signature_path, 'w')
        file.write('---BEGIN OS2 CRYPTO DATA---\n')
        file.write('Description:\n    Signature\n\n')
        file.write('File name:\n    ')
        file.write(self.signature_path)
        file.write('\n\nMethod:\n    ' + hash_function.get() + '\n    ' + asimmetric_alg)
        if asimmetric_alg != 'RSA':
            file.write('\n\nSecret number:\n    ')
            write_to_file(file, str(hex(k).upper()[2:]))
        file.write('\n\nKey length:\n    ')
        file.write(str(hex(len(hash) * 8)).upper().replace('0X', '') + '\n    ')
        file.write(private_key_size)
        file.write('\n\nData:\n    ')
        write_to_file(file, data.decode())
        file.write('\n\nSignature:\n    ')
        write_to_file(file, str(signature).upper().replace('0X', ''))
        file.write('\n\n---END OS2 CRYPTO DATA---')

    def check(self):
        data = get_data(self.signature_path, 'Data')
        data = b64decode(data)
        modulus = int(int(get_data(self.public_key_path, 'Modulus'), 16))
        public_exp = int(int(get_data(self.public_key_path, 'Public exponent').strip(), 16))
        methods = get_methods(self.signature_path).split(':')
        if methods[1] != 'RSA':
            generator = int(int(get_data(self.public_key_path, 'Generator'), 16))
            k = int(int(get_data(self.signature_path, 'Secret number').strip(), 16))
        signature = get_data(self.signature_path, 'Signature')
        signature = int(int(signature, 16))
        m = hashlib.new(methods[0])
        m.update(data)
        hash = m.digest()
        if methods[1] == 'RSA':
            RSAEncryptor = RSA.construct((modulus, public_exp))
            if RSAEncryptor.verify(hash, (signature, '')):
                print("Message is authentic")
                tkinter.messagebox.showinfo("Message is authentic")
            else:
                print("Integrity and authentic are disrupted!")
                tkinter.messagebox.showinfo("Integrity and authentic are disrupted!")
        else:
            ElGamalEncryptor = ElGamal.construct((modulus, generator, public_exp))
            if ElGamalEncryptor.verify(hash, (signature, k)):
                print("Message is authentic")
                tkinter.messagebox.showinfo("Message is authentic")

            else:
                print("Integrity and authentic are disrupted!")
                tkinter.messagebox.showinfo("Integrity and authentic are disrupted!")

    def choose_input(self, key_path):
        choosen = tkinter.filedialog.askopenfilename(initialdir='files')
        self.input_path = choosen
        key_path.set(self.input_path)

    def choose_private_key(self, key_path):
        choosen = tkinter.filedialog.askopenfilename(initialdir='files')
        self.private_key_path = choosen
        key_path.set(self.private_key_path)

    def choose_public_key(self, key_path):
        choosen = tkinter.filedialog.askopenfilename(initialdir='files')
        self.public_key_path = choosen
        key_path.set(self.public_key_path)

    def choose_signature_file(self, key_path):
        choosen = tkinter.filedialog.askopenfilename(initialdir='files')
        self.signature_path = choosen
        key_path.set(self.signature_path)

    def ByteToHex(self, byteStr):
        return ''.join(["%02X" % x for x in byteStr]).strip()

    def HexToByte(self, hexStr):
        return bytes.fromhex(hexStr)
