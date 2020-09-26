from pyDes import des, CBC, PAD_PKCS5
import binascii

def des_encrypt(key,s):
    '''
    des加密，key必须是utf-8,s可以是字符串
    返回值是bytes
    '''
    k = des(key,CBC,key,pad=None, padmode=PAD_PKCS5)
    en = k.encrypt(s,padmode=PAD_PKCS5)
    return binascii.b2a_hex(en)

def des_descrypt(key,s):
    '''
    des解密,返回值是bytes
    '''
    k = des(key,CBC,key,pad=None, padmode=PAD_PKCS5)
    en = k.decrypt(binascii.a2b_hex(s),padmode=PAD_PKCS5)
    return en

if __name__ == "__main__":
    key='12345678'
    s=['test1','test2']
    for i in s:
        e = des_encrypt(key,i)
        d = des_descrypt(key,e)
        print(len(key),key,i,e,d)
# 8 12345678 test1 b'786f7c42a11dcb70' b'test1'
# 8 12345678 test2 b'd9432bace56a4bb9' b'test2'