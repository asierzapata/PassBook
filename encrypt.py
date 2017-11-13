#!/usr/bin/env python
# coding=utf-8

import random
import sys
from Crypto.Cipher import AES

## Cosas a tener en cuenta para la encripcion
##      - Tanto la key como el init vector tienen que tener como size 16, 24 o 32 bytes.
##        Por tanto los valores de longitud validos para la key son
##      - Supondremos que la validacion de la length maxima de la key se hace previamente
##      - Type 1 es encriptar, y el 0 desencriptar

def crypto(msg,key,initvector,type):
    # zfill intenta añadir 0 a la izq hasta el tamaño pasado por parametro. Si este tamaño ya
    # se cumple, devuelve el original

    key = key.zfill(AES.block_size)

    aes = AES.new(key, AES.MODE_CBC, initvector)
    if type == 1:
        return aes.encrypt(msg.zfill(AES.block_size))
    else:
        return aes.decrypt(msg).strip('0')