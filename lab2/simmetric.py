import os
from Crypto.Cipher import AES
from Crypto.Cipher import DES3
from Crypto import Random
from base64 import b64encode, b64decode
import tkinter.filedialog
from util import *


class SimCrypt:
    def __init__(self):
        self.key_path = 'files/sim_kljuc.txt'
        self.input_path = 'files/sim_ulaz.txt'
        self.output_path = 'files/sim_izlaz.txt'

    def choose_key(self, key_path):
        choosen = tkinter.filedialog.askopenfilename(initialdir='files')
        self.key_path = choosen
        key_path.set(self.key_path)

    def encrypt(self, algorithm, mode):
        algorithm = algorithm.get()
        modes = mode.get()
        mode = get_mode(mode.get())
        key = self.HexToByte(get_data(self.key_path, 'Secret key'))
        if (algorithm.split('-')[0].upper() == 'AES'):
            iv = Random.new().read(AES.block_size)
            cipher = AES.new(key, mode, iv)
        else:
            iv = Random.new().read(DES3.block_size)
            cipher = DES3.new(key, mode, iv)
        data = get_data(self.input_path, 'Data')
        if len(data) % cipher.block_size != 0:
            data += ' ' * (cipher.block_size - len(data) % cipher.block_size)
        encoded = cipher.encrypt(data)
        encoded = b64encode(encoded)

        file = open(self.output_path, 'w')
        file.write('---BEGIN OS2 CRYPTO DATA---\n')
        file.write('Description:\n    Crypted file\n\n')
        file.write('Method:\n    ' + algorithm.split('-')[0].upper() + '\n\n')
        file.write('Crypt Method:\n    ' + modes + '\n\n')
        file.write('Key length:\n    ' + str(hex(len(key) * 8)).replace('0x', '') + '\n\n')
        file.write('Initialization vector:\n    ' + str(self.ByteToHex(iv)) + '\n\n')
        file.write('File name:\n    ')
        file.write(self.output_path)
        file.write('\n\nData:\n    ')
        write_to_file(file, encoded.decode())
        file.write('\n\n---END OS2 CRYPTO DATA---')
        tkinter.messagebox.showinfo("Cripted message:", encoded)

    def decrypt(self):
        algorithm = get_data(self.input_path, 'Method')
        mode = get_data(self.input_path, 'Crypt Method')
        key = self.HexToByte(get_data(self.key_path, 'Secret key'))
        iv = self.HexToByte(get_data(self.input_path, 'Initialization vector'))
        mode = get_mode(mode)
        if (algorithm.upper() == 'AES'):
            cipher = AES.new(key, mode, iv)
        else:
            cipher = DES3.new(key, mode, iv)
        data = get_data(self.input_path, 'Data')
        data = b64decode(data)
        decoded = cipher.decrypt(data)
        decoded = decoded.strip()

        file = open(self.output_path, 'w')
        file.write('---BEGIN OS2 CRYPTO DATA---\n')
        file.write('Description:\n    Decrypted file\n\n')
        file.write('File name:\n    ')
        file.write(self.output_path)
        file.write('\n\nData:\n    ')
        write_to_file(file, decoded.decode())
        file.write('\n\n---END OS2 CRYPTO DATA---')

    def choose_input(self, key_path):
        choosen = tkinter.filedialog.askopenfilename(initialdir='files')
        self.input_path = choosen
        key_path.set(self.input_path)

    def choose_output(self, key_path):
        choosen = tkinter.filedialog.askopenfilename(initialdir='files')
        self.output_path = choosen
        key_path.set(self.output_path)

    def generate_key(self, algorithm_name):
        keySize = int(algorithm_name.get().split('-')[1])
        self.key = os.urandom(int(keySize / 8))
        file = open(self.key_path, 'w')
        file.write('---BEGIN OS2 CRYPTO DATA---\n')
        file.write('Description:\n    Secret key\n\n')
        file.write('Method:\n    ' + algorithm_name.get().split('-')[0].upper() + '\n\n')
        file.write('File name:\n    ')
        file.write(self.key_path)
        file.write('\n\nKey length:\n    ' + (str(hex(keySize))).replace('0x', ''))
        file.write('\n\nSecret key:\n    ')
        write_to_file(file, self.ByteToHex(self.key))
        file.write('\n\n---END OS2 CRYPTO DATA---')

    def ByteToHex(self, byteStr):
        return ''.join(["%02X" % x for x in byteStr]).strip()

    def HexToByte(self, hexStr):
        return bytes.fromhex(hexStr)
