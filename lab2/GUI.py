from tkinter import *
import os
import hashes
import simmetric
import asimmetric
import signature
import envelope
import seal

hashObject = hashes.SHA()


def hashWindow():
    win = Toplevel()
    win.geometry('600x300+400+100')

    Label(win, text='Choose hash algorithm:').grid(row=0, column=2, sticky=E)
    var = StringVar()
    var.set("sha1")
    OptionMenu(win, var, "sha1", "sha256", "sha512", "sha3_256", "sha3_512").grid(row=0, column=3)

    Label(win, text='Input:').grid(row=1, column=1)
    input_path = StringVar()
    input_path.set('files/ulaz.txt')
    Entry(win, textvariable=input_path, width=50).grid(row=1, column=2)
    Button(win, text='Choose', command=lambda: hashObject.choose_input(input_path)).grid(row=1, column=3)

    Label(win, text='Output:').grid(row=2, column=1)
    output_path = StringVar()
    output_path.set('files/sazetak.txt')
    Entry(win, textvariable=output_path, width=50).grid(row=2, column=2)
    Button(win, text='Choose', command=lambda: hashObject.choose_output(output_path)).grid(row=2, column=3)

    Button(win, text='Generate hash', command=lambda: hashObject.generate(var.get())).grid(row=3, column=2)


simObject = simmetric.SimCrypt()


def simWindow():
    win = Toplevel()
    win.geometry('600x300+400+100')

    Label(win, text='Choose simmetric algorithm:').grid(row=0, column=2, sticky=E)
    algorithm = StringVar()
    algorithm.set("aes-128")
    OptionMenu(win, algorithm, "aes-128", "aes-192", "aes-256", "des3-128", "des3-192").grid(row=0, column=3)

    Label(win, text='Choose mode:').grid(row=1, column=2, sticky=E)
    crypt_method = StringVar()
    crypt_method.set("ECB")
    OptionMenu(win, crypt_method, "ECB", "CBC", "OFB", "CFB").grid(row=1, column=3)

    Label(win, text='Key:').grid(row=2, column=1)
    key_path = StringVar()
    key_path.set('files/sim_kljuc.txt')
    kljucEntry = Entry(win, textvariable=key_path, width=50)
    kljucEntry.grid(row=2, column=2)
    Button(win, text='Choose', command=lambda: simObject.choose_key(key_path)).grid(row=2, column=3)
    Button(win, text='Generate', command=lambda: simObject.generate_key(algorithm)).grid(row=2, column=5)

    Label(win, text="Input:").grid(row=3, column=1)
    input_path = StringVar()
    input_path.set('files/sim_ulaz.txt')
    Entry(win, textvariable=input_path, width=50).grid(row=3, column=2)
    Button(win, text='Choose', command=lambda: simObject.choose_input(input_path)).grid(row=3, column=3)

    Label(win, text="Output:").grid(row=4, column=1)
    output_path = StringVar()
    output_path.set('files/sim_izlaz.txt')
    Entry(win, textvariable=output_path, width=50).grid(row=4, column=2)
    Button(win, text='Choose', command=lambda: simObject.choose_output(output_path)).grid(row=4, column=3)

    Button(win, text='Decrypt', command=lambda: simObject.decrypt()).grid(row=6, column=3)
    Button(win, text='Encrypt', command=lambda: simObject.encrypt(algorithm, crypt_method)).grid(row=6, column=2)


asimObject = asimmetric.ASimCrypt()


def asimWindow():
    win = Toplevel()
    win.geometry('600x300+400+100')

    Label(win, text='Choose asimmetric algorithm:').grid(row=0, column=2, sticky=E)
    algorithm = StringVar()
    algorithm.set("RSA")
    OptionMenu(win, algorithm, "RSA", "ElGamal").grid(row=0, column=3)

    Label(win, text='Public key:').grid(row=1, column=1)
    public_key_path = StringVar()
    public_key_path.set('files/asim_public_key.txt')
    Entry(win, textvariable=public_key_path, width=50).grid(row=1, column=2)
    Button(win, text='Choose', command=lambda: asimObject.choose_public(public_key_path)).grid(row=1, column=3)

    Label(win, text="Private key:").grid(row=2, column=1)
    private_key_path = StringVar()
    private_key_path.set('files/asim_private_key.txt')
    Entry(win, textvariable=private_key_path, width=50).grid(row=2, column=2)
    Button(win, text='Choose', command=lambda: asimObject.choose_private(private_key_path)).grid(row=2, column=3)

    keySize = IntVar()
    keySize.set(1024)
    Radiobutton(win, text='1024', value=1024,
                variable=keySize).grid(row=5, column=2)
    Radiobutton(win, text='2048', value=2048,
                variable=keySize).grid(row=5, column=3)
    Radiobutton(win, text='4096', value=4096,
                variable=keySize).grid(row=5, column=4)
    Button(win, text='Generate key pair', command=lambda: asimObject.generate(keySize, algorithm)).grid(row=7, column=3)


signObject = signature.Signature()


def signWindow():
    win = Toplevel()
    win.geometry('600x300+400+100')

    Label(win, text='Choose hash algorithm:').grid(row=0, column=2, sticky=E)
    hash_function = StringVar()
    hash_function.set("sha1")
    OptionMenu(win, hash_function, "sha1", "sha256", "sha512", "sha3_256", "sha3_512").grid(row=0, column=3)

    Label(win, text='Input:').grid(row=1, column=1)
    input_path = StringVar()
    Entry(win, textvariable=input_path, width=50).grid(row=1, column=2)
    input_path.set('files/ulaz.txt')
    Button(win, text='Choose', command=lambda: signObject.choose_input(input_path)).grid(row=1, column=3)

    Label(win, text="Sender private key:").grid(row=2, column=1)
    private_key_path = StringVar()
    Entry(win, textvariable=private_key_path, width=50).grid(row=2, column=2)
    private_key_path.set('files/asim_private_key.txt')
    Button(win, text='Choose', command=lambda: signObject.choose_private_key(private_key_path)).grid(row=2, column=3)

    Label(win, text="Digital signature:").grid(row=3, column=1)
    signature_path = StringVar()
    Entry(win, textvariable=signature_path, width=50).grid(row=3, column=2)
    signature_path.set('files/signature.txt')
    Button(win, text='Choose', command=lambda: signObject.choose_signature_file(signature_path)).grid(row=3, column=3)

    Button(win, text='Generate digital signature', command=lambda: signObject.generate(hash_function)).grid(row=4,
                                                                                                            column=1,
                                                                                                            columnspan=2)

    message = "Sender public key:"
    Label(win, text=message).grid(row=5, column=1)
    public_key_path = StringVar()
    Entry(win, textvariable=public_key_path, width=50).grid(row=5, column=2)
    public_key_path.set('files/asim_public_key.txt')
    Button(win, text='Choose', command=lambda: signObject.choose_public_key(public_key_path)).grid(row=5, column=3)

    Button(win, text='Check digital singature', command=signObject.check).grid(row=7, column=1, columnspan=2)


envObject = envelope.Envelope()


def envelopeWindow():
    win = Toplevel()
    win.geometry('600x300+400+100')

    Label(win, text="Input:").grid(row=1, column=1)
    input_path = StringVar()
    Entry(win, textvariable=input_path, width=50).grid(row=1, column=2)
    input_path.set('files/ulaz.txt')
    Button(win, text='Choose', command=lambda: envObject.choose_input(input_path)).grid(row=1, column=3)

    Label(win, text='Choose simmetric algorithm:').grid(row=2, column=2, sticky=E)
    algorithm = StringVar()
    algorithm.set("aes-128")
    OptionMenu(win, algorithm, "aes-128", "aes-192", "aes-256", "des3-128", "des3-192").grid(row=2, column=3)

    Label(win, text='Choose mode:').grid(row=3, column=2, sticky=E)
    crypt_method = StringVar()
    crypt_method.set("ECB")
    OptionMenu(win, crypt_method, "ECB", "CBC", "OFB", "CFB").grid(row=3, column=3)

    Label(win, text='Sender simmetric key:').grid(row=4, column=1)
    key_path = StringVar()
    key_path.set('files/sim_kljuc.txt')
    Entry(win, textvariable=key_path, width=50).grid(row=4, column=2)
    Button(win, text='Choose', command=lambda: envObject.choose_sim_key(key_path)).grid(row=4, column=3)
    Button(win, text='Generate', command=lambda: simObject.generate_key(algorithm)).grid(row=4, column=5)

    message = "Receiver public key:"
    Label(win, text=message).grid(row=5, column=1)
    public_key_path = StringVar()
    Entry(win, textvariable=public_key_path, width=50).grid(row=5, column=2)
    public_key_path.set('files/asim_public_key.txt')
    Button(win, text='Choose', command=lambda: envObject.choose_public_key(public_key_path)).grid(row=5, column=3)

    Label(win, text="Digital envelope:").grid(row=6, column=1)
    envelope_path = StringVar()
    Entry(win, textvariable=envelope_path, width=50).grid(row=6, column=2)
    envelope_path.set('files/envelope.txt')
    Button(win, text='Choose', command=lambda: envObject.choose_envelope_file(envelope_path)).grid(row=6, column=3)

    Button(win, text='Generate digital envelope', command=lambda: envObject.generate(algorithm, crypt_method)).grid(
        row=7, column=1,
        columnspan=2)

    Label(win, text="Receiver private key:").grid(row=8, column=1)
    private_key_path = StringVar()
    Entry(win, textvariable=private_key_path, width=50).grid(row=8, column=2)
    private_key_path.set('files/asim_private_key.txt')
    Button(win, text='Choose', command=lambda: envObject.choose_private_key(private_key_path)).grid(row=8, column=3)

    Label(win, text="Output:").grid(row=9, column=1)
    output_path = StringVar()
    Entry(win, textvariable=output_path, width=50).grid(row=9, column=2)
    output_path.set('files/env_output.txt')
    Button(win, text='Choose', command=lambda: envObject.choose_output(output_path)).grid(row=9, column=3)

    Button(win, text='Open digital envelope', command=lambda: envObject.open_envelope()).grid(row=10, column=1,
                                                                                              columnspan=2)


sealObject = seal.Seal()


def sealWindow():
    win = Toplevel()
    win.geometry('600x400+400+100')

    Label(win, text="Input:").grid(row=1, column=1)
    input_path = StringVar()
    Entry(win, textvariable=input_path, width=50).grid(row=1, column=2)
    input_path.set('files/ulaz.txt')
    Button(win, text='Choose', command=lambda: envObject.choose_input(input_path)).grid(row=1, column=3)

    Label(win, text='Choose simmetric algorithm:').grid(row=2, column=2, sticky=E)
    algorithm = StringVar()
    algorithm.set("aes-128")
    OptionMenu(win, algorithm, "aes-128", "aes-192", "aes-256", "des3-128", "des3-192").grid(row=2, column=3)

    Label(win, text='Choose mode:').grid(row=3, column=2, sticky=E)
    crypt_method = StringVar()
    crypt_method.set("ECB")
    OptionMenu(win, crypt_method, "ECB", "CBC", "OFB", "CFB").grid(row=3, column=3)

    Label(win, text='Sender simmetric key:').grid(row=4, column=1)
    key_path = StringVar()
    key_path.set('files/sim_kljuc.txt')
    Entry(win, textvariable=key_path, width=50).grid(row=4, column=2)
    Button(win, text='Choose', command=lambda: envObject.choose_sim_key(key_path)).grid(row=4, column=3)
    Button(win, text='Generate', command=lambda: simObject.generate_key(algorithm)).grid(row=4, column=5)

    message = "Sender private key:"
    Label(win, text=message).grid(row=5, column=1)
    private_a_key_path = StringVar()
    Entry(win, textvariable=private_a_key_path, width=50).grid(row=5, column=2)
    private_a_key_path.set('files/asim_a_private_key.txt')
    Button(win, text='Choose', command=lambda: sealObject.choose_private_a_key(private_a_key_path)).grid(row=5,
                                                                                                         column=3)

    message = "Receiver public key:"
    Label(win, text=message).grid(row=6, column=1)
    public_b_key_path = StringVar()
    Entry(win, textvariable=public_b_key_path, width=50).grid(row=6, column=2)
    public_b_key_path.set('files/asim_public_b_key.txt')
    Button(win, text='Choose', command=lambda: sealObject.choose_public_b_key(public_b_key_path)).grid(row=6, column=3)

    Label(win, text='Choose hash algorithm:').grid(row=7, column=2, sticky=E)
    hash_function = StringVar()
    hash_function.set("sha1")
    OptionMenu(win, hash_function, "sha1", "sha256", "sha512", "sha3_256", "sha3_512").grid(row=7, column=3)

    Label(win, text="Digital seal:").grid(row=8, column=1)
    seal_path = StringVar()
    Entry(win, textvariable=seal_path, width=50).grid(row=8, column=2)
    seal_path.set('files/seal.txt')
    Button(win, text='Choose', command=lambda: envObject.choose_envelope_file(seal_path)).grid(row=8, column=3)

    Button(win, text='Generate digital seal',
           command=lambda: sealObject.generate(algorithm.get(), crypt_method.get(), hash_function.get())).grid(row=9,
                                                                                                               column=1,
                                                                                                               columnspan=2)
    # ===============================
    Label(win, text="Sender public key:").grid(row=10, column=1)
    public_a_key_path = StringVar()
    Entry(win, textvariable=public_a_key_path, width=50).grid(row=10, column=2)
    public_a_key_path.set('files/asim_a_public_key.txt')
    Button(win, text='Choose', command=lambda: sealObject.choose_public_a_key(public_a_key_path)).grid(row=10, column=3)

    Label(win, text="Receiver private key:").grid(row=11, column=1)
    private_b_key_path = StringVar()
    Entry(win, textvariable=private_b_key_path, width=50).grid(row=11, column=2)
    private_b_key_path.set('files/asim_b_private_key.txt')
    Button(win, text='Choose', command=lambda: sealObject.choose_private_b_key(private_b_key_path)).grid(row=11,
                                                                                                         column=3)

    Label(win, text="Output:").grid(row=12, column=1)
    output_path = StringVar()
    Entry(win, textvariable=output_path, width=50).grid(row=12, column=2)
    output_path.set('files/seal_output.txt')
    Button(win, text='Choose', command=lambda: sealObject.choose_output(output_path)).grid(row=12, column=3)

    Button(win, text='Open digital seal', command=lambda: sealObject.open_seal()).grid(row=13, column=1,
                                                                                     columnspan=2)


root = Tk(baseName='GUI')
root.geometry('200x200+100+100')
button1 = Button(master=root, text='Hash', command=hashWindow)
button1.grid(row=1, column=1, sticky=W + E + N + S)
button2 = Button(master=root, text='Simetric Crypt', command=simWindow).grid(row=2, column=1)
button3 = Button(master=root, text='Asimetric Crypt', command=asimWindow).grid(row=3, column=1)
button4 = Button(master=root, text='Digital signature', command=signWindow).grid(row=4, column=1)
button5 = Button(master=root, text='Digital envelope', command=envelopeWindow).grid(row=5, column=1)
button6 = Button(master=root, text='Digital seal', command=sealWindow).grid(row=6, column=1)

root.mainloop()
