""" coding: utf-8
Created by rsanchez on 03/05/2018
Este proyecto ha sido desarrollado en la Gerencia de Operaciones de CENACE
Mateo633
"""
import base64
from Crypto import Random
from Crypto.Cipher import AES

default_key = b'\xbf\xc0\x85)\x10nc\x98\x02)j\xdf\xcb\xc4\x98\x9d(\x9e[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18'


def pad(s):
    return bytes(s, "utf8") + b"\0" * (AES.block_size - len(s) % AES.block_size)


def encrypt(message, key=default_key):
    message = pad(message)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return base64.urlsafe_b64encode(iv + cipher.encrypt(message)).decode('utf8')


def decrypt(ciphertext, key=default_key):
    ciphertext = base64.urlsafe_b64decode(bytes(ciphertext, 'utf8'))
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b"\0").decode("utf-8")


def encrypt_file(file_name, key=default_key):
    with open(file_name, 'rb') as fo:
        plaintext = fo.read()
    enc = encrypt(plaintext, key=key)
    with open(file_name + ".enc", 'wb') as fo:
        fo.write(enc)


def decrypt_file(file_name, key=default_key):
    with open(file_name, 'rb') as fo:
        ciphertext = fo.read()
    dec = decrypt(ciphertext, key=key)
    with open(file_name[:-4], 'wb') as fo:
        fo.write(dec)


def encrypt_tag_obj(obj_w_tag):

    if isinstance(obj_w_tag, dict):
        if 'tag' in obj_w_tag.keys():
            obj_w_tag['tag'] = encrypt(obj_w_tag['tag'], default_key)
            return obj_w_tag

    if isinstance(obj_w_tag, list):
        for d in obj_w_tag:
            if 'tag' in d.keys():
                d['tag'] = encrypt(d['tag'], default_key)
        return obj_w_tag


def decrypt_tag_obj(obj_w_tag):

    if isinstance(obj_w_tag, dict):
        if 'tag' in obj_w_tag.keys():
            obj_w_tag.tag = decrypt(obj_w_tag.tag, default_key)

    if isinstance(obj_w_tag, list):
        for d in obj_w_tag:
            if 'tag' in d.keys():
                d['tag'] = decrypt(d['tag'], default_key)
        return obj_w_tag

# TEST:
# encrypt_file('to_enc.txt', key)
# text = "hola este es un codigo sin encriptar"
# text_encriptado = encrypt(text, key)
# text_desencriptado = decrypt(text_encriptado, key)
# print(text_encriptado, text_desencriptado)
