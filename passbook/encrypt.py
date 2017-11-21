#!/usr/bin/env python
# coding=utf-8

from Crypto.Cipher import AES

## Important considerations to keep in mind about the encryption
##      - Both key and init vector must have sizes equal to 16, 24 or 32 bytes.
##      - We will asume that validation of max length is already done at this point of the code
##      - Type 1 is for encrypting and 0 for decrypting
##

def crypto(msg,key,initvector,type):

    # with zfill we do a zero padding of max length of the block size
    key = key.zfill(AES.block_size)

    aes = AES.new(key, AES.MODE_CBC, initvector)
    if type == 1:
        return aes.encrypt(msg.zfill(AES.block_size))
    else:
        return aes.decrypt(msg).strip('0')