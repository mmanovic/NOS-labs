from base64 import b64encode, b64decode
import hashlib
import os
import tkinter.filedialog
import tkinter.messagebox
import util


class SHA:
    def __init__(self):
        self.input_path = 'files/ulaz.txt'
        self.output_path = 'files/sazetak.txt'

    def generate(self, algorithm_name):
        data = util.get_data(self.input_path, 'Data')
        m = hashlib.new(algorithm_name)
        m.update(data.encode(encoding='utf-8'))
        hash = m.digest()
        hash = self.ByteToHex(hash)
        file = open(self.output_path, 'w')
        file.write('---BEGIN OS2 CRYPTO DATA---\n')
        file.write('Description:\n    Digest\n\n')
        file.write('File name:\n    ')
        file.write(self.output_path)
        file.write('\nMethod:\n    ' + algorithm_name + '\n\n')
        file.write('Key length:\n    ')
        file.write(str(hex(len(hash) * 4)).upper().replace('0X', '') + '\n')
        file.write('\nDigest:\n    ')
        i = 1
        for c in hash:
            if i == 61:
                file.write('\n    ')
                i = 1
            file.write(c)
            i += 1
        file.write('\n\n---END OS2 CRYPTO DATA---')
        tkinter.messagebox.showinfo("Sazetak:", hash)

    def choose_input(self, key_path):
        choosen = tkinter.filedialog.askopenfilename(initialdir='files')
        self.input_path = choosen
        key_path.set(self.input_path)

    def choose_output(self, key_path):
        choosen = tkinter.filedialog.askopenfilename(initialdir='files')
        self.output_path = choosen
        key_path.set(self.output_path)

    def ByteToHex(self, byteStr):
        return ''.join(["%02X" % x for x in byteStr]).strip()

    def HexToByte(self, hexStr):
        bytes = []
        hexStr = ''.join(hexStr.split(" "))
        for i in range(0, len(hexStr), 2):
            bytes.append(chr(int(hexStr[i:i + 2], 16)))
        return ''.join(bytes)
