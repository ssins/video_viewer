from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
 
 
class PrpCrypt(object):
 
    def __init__(self, key):
        self.key = key.encode('utf-8')
        self.mode = AES.MODE_CBC
 
    def encrypt(self, text):
        text = text.encode('utf-8')
        cryptor = AES.new(self.key, self.mode, b'0000000000000000')
        # 这里密钥key 长度必须为16（AES-128）,
        # 24（AES-192）,或者32 （AES-256）Bytes 长度
        length = 32
        count = len(text)
        if count < length:
            add = (length - count)
            text = text + ('\0' * add).encode('utf-8')
        elif count > length:
            add = (length - (count % length))
            text = text + ('\0' * add).encode('utf-8')
        self.ciphertext = cryptor.encrypt(text)
        return b2a_hex(self.ciphertext)
 
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, b'0000000000000000')
        plain_text = cryptor.decrypt(a2b_hex(text))
        return bytes.decode(plain_text).rstrip('\0')
 
 
# if __name__ == '__main__':
#     pc = PrpCrypt('keyskeyskeyskeys')
#     e = pc.encrypt("testtesttest")
#     d = pc.decrypt(e)
#     print("加密:", e)
#     print("解密:", d)