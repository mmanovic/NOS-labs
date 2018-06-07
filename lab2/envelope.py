import os
from Crypto.Cipher import AES
from Crypto.Cipher import DES3
from Crypto.PublicKey import ElGamal
from Crypto.PublicKey import RSA
from Crypto.Util.number import GCD
from Crypto import Random
from Crypto.Random import random
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64encode, b64decode
import tkinter.messagebox
import tkinter.filedialog
from util import *


class Envelope:
    def __init__(self):
        self.input_path = 'files/ulaz.txt'
        self.private_key_path = 'files/asim_private_key.txt'
        self.public_key_path = 'files/asim_public_key.txt'
        self.output_path = 'files/env_output.txt'
        self.envelope_path = 'files/envelope.txt'
        self.sim_key_path = 'files/sim_kljuc.txt'

    def generate(self, algorithm, mode):
        algorithm = algorithm.get()
        modes = mode.get()
        mode = get_mode(mode.get())
        sim_key = self.HexToByte(get_data(self.sim_key_path, 'Secret key'))

        if (algorithm.split('-')[0].upper() == 'AES'):
            iv = Random.new().read(AES.block_size)
            cipher = AES.new(sim_key, mode, iv)
        else:
            iv = Random.new().read(DES3.block_size)
            cipher = DES3.new(sim_key, mode, iv)
        data = get_data(self.input_path, 'Data')
        if len(data) % cipher.block_size != 0:
            data += ' ' * (cipher.block_size - len(data) % cipher.block_size)
        encoded = cipher.encrypt(data)
        encoded = b64encode(encoded)

        modulus = int(int(get_data(self.public_key_path, 'Modulus'), 16))
        public_exp = int(int(get_data(self.public_key_path, 'Public exponent').strip(), 16))
        asimmetric_alg = get_data(self.public_key_path, 'Method')
        if asimmetric_alg != 'RSA':
            generator = int(int(get_data(self.public_key_path, 'Generator'), 16))

        if (asimmetric_alg == 'RSA'):
            RSAEncryptor = RSA.construct((modulus, public_exp))
            encrypted_key = RSAEncryptor.encrypt(sim_key, '')
            encrypted_key = encrypted_key[0]
        else:
            ElGamalEncryptor = ElGamal.construct((modulus, generator, public_exp))
            while 1:
                k = random.StrongRandom().randint(1, modulus - 1)
                if GCD(k, modulus - 1) == 1: break
            encrypted_key = ElGamalEncryptor.encrypt(sim_key, int(k))
            k = encrypted_key[1]
            encrypted_key = encrypted_key[0]

        file = open(self.envelope_path, 'w')
        file.write('---BEGIN OS2 CRYPTO DATA---\n')
        file.write('Description:\n    Envelope\n\n')
        file.write('File name:\n    ')
        file.write(self.envelope_path)
        file.write('\n\nMethod:\n    ' + algorithm.split('-')[0].upper() + '\n    ' + asimmetric_alg + '\n\n')
        if asimmetric_alg != 'RSA':
            file.write('Secret number:\n    ')
            write_to_file(file, self.ByteToHex(k))
        file.write('\n\nCrypt Method:\n    ' + modes + '\n\n')
        file.write('Initialization vector:\n    ' + str(self.ByteToHex(iv)))
        file.write('\n\nKey length:\n    ' + str(hex(len(sim_key) * 8)).replace('0x', '') + '\n    ')
        file.write(get_data(self.public_key_path, 'Key length'))
        file.write('\n\nEnvelope data:\n    ')
        write_to_file(file, encoded.decode())
        file.write('\n\nEnvelope crypt key:\n    ')
        write_to_file(file, self.ByteToHex(encrypted_key))
        file.write('\n\n---END OS2 CRYPTO DATA---')

    def open_envelope(self):
        envelope_data = b64decode(get_data(self.envelope_path, 'Envelope data'))
        crypt_key = self.HexToByte(get_data(self.envelope_path, 'Envelope crypt key'))
        private_exp = int(int(get_data(self.private_key_path, 'Private exponent'), 16))
        public_exp = int(int(get_data(self.public_key_path, 'Public exponent'), 16))
        crypt_method = get_mode(get_data(self.envelope_path, 'Crypt Method'))
        methods = get_methods(self.envelope_path).split(':')
        modulus = int(int(get_data(self.private_key_path, 'Modulus'), 16))
        iv = self.HexToByte(get_data(self.envelope_path, 'Initialization vector'))
        if methods[1] == 'RSA':
            RSAEncryptor = RSA.construct((modulus, public_exp, private_exp))
            decrypted_key = RSAEncryptor.decrypt((crypt_key, ''))
        else:
            generator = int(int(get_data(self.private_key_path, 'Generator'), 16))
            k = self.HexToByte(get_data(self.envelope_path, 'Secret number').lower().strip())
            ElGamalEncryptor = ElGamal.construct((modulus, generator, public_exp, private_exp))
            decrypted_key = ElGamalEncryptor.decrypt((crypt_key, k))
        if (methods[0] == 'AES'):
            cipher = AES.new(decrypted_key, crypt_method, iv)
            data = cipher.decrypt(envelope_data)
        else:
            cipher = DES3.new(decrypted_key, crypt_method, iv)
            data = cipher.decrypt(envelope_data)

        # zapisivanje data-e
        file = open(self.output_path, 'w')
        file.write('---BEGIN OS2 CRYPTO DATA---\n')
        file.write('Description:\n    Decrypted Envelope\n\n')
        file.write('File name:\n    ')
        file.write(self.output_path)
        file.write('\n\nMethod:\n    ' + methods[0] + '\n    ' + methods[1] + '\n\n')
        file.write('Data:\n    ')
        write_to_file(file, data.decode())
        file.write('\n\n---END OS2 CRYPTO DATA---')

    def choose_sim_key(self, key_path):
        choosen = tkinter.filedialog.askopenfilename(initialdir='files')
        self.sim_key_path = choosen
        key_path.set(self.sim_key_path)

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

    def choose_envelope_file(self, key_path):
        choosen = tkinter.filedialog.askopenfilename(initialdir='files')
        self.envelope_path = choosen
        key_path.set(self.envelope_path)

    def choose_output(self, key_path):
        choosen = tkinter.filedialog.askopenfilename(initialdir='files')
        self.output_path = choosen
        key_path.set(self.output_path)

    def ByteToHex(self, byteStr):
        return ''.join(["%02X" % x for x in byteStr]).strip()

    def HexToByte(self, hexStr):
        return bytes.fromhex(hexStr)
