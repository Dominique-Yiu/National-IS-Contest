import base64
import binascii

import numpy as np
from gmssl import sm2, func

class encrypt:
    def __init__(self):
        self.private_key='00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
        self.public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
        self.sm2_crypt = sm2.CryptSM2(public_key=self.public_key, private_key=self.private_key)
    def encryption(self,data=None):
        enc_data=self.sm2_crypt.encrypt(data)
        return enc_data
    def decryption(self,enc_data=None):
        dec_data = self.sm2_crypt.decrypt(enc_data)
        return dec_data

#数据和加密后数据为bytes类型

# _encrypt = encrypt()
# data=b'123456'
# enc_data=_encrypt.encryption(data)
# print(enc_data)
# with open("pin.txt", "wb") as f:
#     f.write(enc_data)
# with open("pin.txt", "rb") as f:
#     enc_data = f.read()
# print(enc_data)
# print(str_enc_data)
# print(_encrypt.decryption(enc_data))