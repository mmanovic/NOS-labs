import os
from Crypto.Cipher import AES
from Crypto.Cipher import DES3
from Crypto.PublicKey import ElGamal
from Crypto.PublicKey import RSA
from Crypto.Util.number import GCD
from Crypto.Random import random
from Crypto import Random
import hashlib
from base64 import b64encode, b64decode
import tkinter.messagebox
import tkinter.filedialog
from util import *


class Seal:
    def __init__(self):
        self.input_path = 'files/ulaz.txt'
        self.private_a_key_path = 'files/asim_a_private_key.txt'
        self.public_a_key_path = 'files/asim_a_public_key.txt'
        self.private_b_key_path = 'files/asim_b_private_key.txt'
        self.public_b_key_path = 'files/asim_b_public_key.txt'
        self.output_path = 'files/seal_output.txt'
        self.seal_path = 'files/seal.txt'
        self.sim_key_path = 'files/sim_kljuc.txt'

    def generate(self, algorithm, mode, hash_function):
        modes = mode
        mode = get_mode(mode)
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

        modulus_b = int(int(get_data(self.public_b_key_path, 'Modulus'), 16))
        public_exp_b = int(int(get_data(self.public_b_key_path, 'Public exponent').strip(), 16))
        asimmetric_alg_b = get_data(self.public_b_key_path, 'Method')
        if (asimmetric_alg_b == 'RSA'):
            RSAEncryptor = RSA.construct((modulus_b, public_exp_b))
            encrypted_key = RSAEncryptor.encrypt(sim_key, '')
            self.envelope_second_part = ''
            encrypted_key = encrypted_key[0]
        else:
            generator_b = int(int(get_data(self.public_b_key_path, 'Generator'), 16))
            ElGamalEncryptor = ElGamal.construct((modulus_b, generator_b, public_exp_b))
            while 1:
                kb = random.StrongRandom().randint(1, modulus_b - 1)
                if GCD(kb, modulus_b - 1) == 1: break
            encrypted_key = ElGamalEncryptor.encrypt(sim_key, kb)
            kb = encrypted_key[1]
            encrypted_key = encrypted_key[0]

        envelope = encoded + encrypted_key
        m = hashlib.new(hash_function)
        m.update(envelope)
        hash = m.digest()
        encoded = b64encode(encoded)

        asimmetric_alg_a = get_data(self.private_a_key_path, 'Method')
        modulus_a = int(int(get_data(self.private_a_key_path, 'Modulus'), 16))
        public_exp_a = int(int(get_data(self.public_a_key_path, 'Public exponent').strip(), 16))
        private_exp_a = int(int(get_data(self.private_a_key_path, 'Private exponent'), 16))
        if (asimmetric_alg_a == 'RSA'):
            RSAEncryptor = RSA.construct((modulus_a, public_exp_a, private_exp_a))
            signature = RSAEncryptor.sign(hash, '')[0]
        else:
            generator_a = int(int(get_data(self.private_a_key_path, 'Generator'), 16))
            ElGamalEncryptor = ElGamal.construct((modulus_a, generator_a, public_exp_a, private_exp_a))
            while 1:
                ka = random.StrongRandom().randint(1, modulus_a - 1)
                if GCD(ka, modulus_a - 1) == 1: break
            signature = ElGamalEncryptor.sign(hash, ka)
            ka = signature[1]
            signature = signature[0]

        file = open(self.seal_path, 'w')
        file.write('---BEGIN OS2 CRYPTO DATA---\n')
        file.write('Description:\n    Seal\n\n')
        file.write('File name:\n    ')
        file.write(self.seal_path)
        file.write('\n\nMethod:\n    ' + algorithm.split('-')[0].upper() + '\n    ' + asimmetric_alg_a + '\n    '
                   + asimmetric_alg_b + '\n    ' + hash_function + '\n\n')
        file.write('Key length:\n    ')
        file.write(get_data(self.sim_key_path, 'Key length') + '\n    ')
        file.write(get_data(self.private_a_key_path, 'Key length') + '\n    ')
        file.write(get_data(self.public_b_key_path, 'Key length') + '\n    ')
        file.write(str(hex(len(hash) * 8)).upper().replace('0X', ''))
        if asimmetric_alg_a != 'RSA':
            file.write('\n\nSignature secret number:\n    ')
            write_to_file(file, str(hex(ka)).upper().replace('0X',''))
        if asimmetric_alg_b != 'RSA':
            file.write('\n\nEnvelope secret number:\n    ')
            write_to_file(file, self.ByteToHex(kb))
        file.write('\n\nCrypt Method:\n    ' + modes + '\n\n')
        file.write('Initialization vector:\n    ' + str(self.ByteToHex(iv)))
        file.write('\n\nEnvelope data:\n    ')
        write_to_file(file, encoded.decode())
        file.write('\n\nEnvelope crypt key:\n    ')
        write_to_file(file, self.ByteToHex(encrypted_key))
        file.write('\n\nSignature:\n    ')
        write_to_file(file, str(hex(signature)).upper().replace('0X', ''))
        file.write('\n\n---END OS2 CRYPTO DATA---')

    def open_seal(self):
        envelope_data = b64decode(get_data(self.seal_path, 'Envelope data'))
        crypt_key = self.HexToByte(get_data(self.seal_path, 'Envelope crypt key'))
        data = envelope_data + crypt_key
        modulus_a = int(int(get_data(self.public_a_key_path, 'Modulus'), 16))
        public_exp_a = int(int(get_data(self.public_a_key_path, 'Public exponent').strip(), 16))
        methods = get_methods(self.seal_path).split(':')
        signature = get_data(self.seal_path, 'Signature')
        signature = int(int(signature, 16))
        m = hashlib.new(methods[3])
        m.update(data)
        hash = m.digest()
        if methods[1] == 'RSA':
            RSAEncryptor = RSA.construct((modulus_a, public_exp_a))
            if RSAEncryptor.verify(hash, (signature, '')):
                print("Message is authentic")
                tkinter.messagebox.showinfo("Message is authentic")
            else:
                print("Integrity and authentic are disrupted!")
                tkinter.messagebox.showinfo("Integrity and authentic are disrupted!")
        else:
            generator_a = int(int(get_data(self.public_a_key_path, 'Generator'), 16))
            ka = int(int(get_data(self.seal_path, 'Signature secret number').strip(), 16))
            ElGamalEncryptor = ElGamal.construct((modulus_a, generator_a, public_exp_a))
            if ElGamalEncryptor.verify(hash, (signature, ka)):
                print("Message is authentic")
                tkinter.messagebox.showinfo("Message is authentic")

            else:
                print("Integrity and authentic are disrupted!")
                tkinter.messagebox.showinfo("Integrity and authentic are disrupted!")

        private_exp_b = int(int(get_data(self.private_b_key_path, 'Private exponent'), 16))
        public_exp_b = int(int(get_data(self.public_b_key_path, 'Public exponent'), 16))
        crypt_method = get_mode(get_data(self.seal_path, 'Crypt Method'))
        modulus_b = int(int(get_data(self.private_b_key_path, 'Modulus'), 16))
        iv = self.HexToByte(get_data(self.seal_path, 'Initialization vector'))
        if methods[2] == 'RSA':
            RSAEncryptor = RSA.construct((modulus_b, public_exp_b, private_exp_b))
            decrypted_key = RSAEncryptor.decrypt((crypt_key, ''))
        else:
            generator_b = int(int(get_data(self.private_b_key_path, 'Generator'), 16))
            kb = self.HexToByte(get_data(self.seal_path, 'Envelope secret number').lower().strip())
            ElGamalEncryptor = ElGamal.construct((modulus_b, generator_b, public_exp_b, private_exp_b))
            decrypted_key = ElGamalEncryptor.decrypt((crypt_key, kb))

        if (methods[0] == 'AES'):
            cipher = AES.new(decrypted_key, crypt_method, iv)
            data = cipher.decrypt(envelope_data)
        else:
            cipher = DES3.new(decrypted_key, crypt_method, iv)
            data = cipher.decrypt(envelope_data)
            # zapisivanje data-e
        file = open(self.output_path, 'w')
        file.write('---BEGIN OS2 CRYPTO DATA---\n')
        file.write('Description:\n    Decrypted Seal\n\n')
        file.write('File name:\n    ')
        file.write(self.output_path)
        file.write('\n\nMethod:\n    ' + methods[0] + '\n    ' + methods[1] + '\n    '
                   + methods[2] + '\n    ' + methods[3] + '\n\n')
        file.write('Data:\n    ')
        write_to_file(file, data.decode())
        file.write('\n\n---END OS2 CRYPTO DATA---')

    def choose_input(self, key_path):
        choosen = tkinter.filedialog.askopenfilename(initialdir='files')
        self.input_path = choosen
        key_path.set(self.input_path)

    def choose_output(self, key_path):
        choosen = tkinter.filedialog.askopenfilename(initialdir='files')
        self.output_path = choosen
        key_path.set(self.output_path)

    def choose_private_a_key(self, key_path):
        choosen = tkinter.filedialog.askopenfilename(initialdir='files')
        self.private_a_key_path = choosen
        key_path.set(self.private_a_key_path)

    def choose_public_a_key(self, key_path):
        choosen = tkinter.filedialog.askopenfilename(initialdir='files')
        self.public_a_key_path = choosen
        key_path.set(self.public_a_key_path)

    def choose_private_b_key(self, key_path):
        choosen = tkinter.filedialog.askopenfilename(initialdir='files')
        self.private_b_key_path = choosen
        key_path.set(self.private_b_key_path)

    def choose_public_b_key(self, key_path):
        choosen = tkinter.filedialog.askopenfilename(initialdir='files')
        self.public_b_key_path = choosen
        key_path.set(self.public_b_key_path)

    def choose_seal_file(self, key_path):
        choosen = tkinter.filedialog.askopenfilename(initialdir='files')
        self.seal_path = choosen
        key_path.set(self.seal_path)

    def choose_sim_key(self, key_path):
        choosen = tkinter.filedialog.askopenfilename(initialdir='files')
        self.sim_key_path = choosen
        key_path.set(self.sim_key_path)

    def ByteToHex(self, byteStr):
        return ''.join(["%02X" % x for x in byteStr]).strip()

    def HexToByte(self, hexStr):
        return bytes.fromhex(hexStr)
