# PassBook

Telegram Bot used to store encripted passwords in mongodb using a key defined by the user, to help remember multiple passwords using only one.

The encryption is made with AES in CBC mode using a library called pycrypto.

## Install 

Modify settings.json with your init vector and credentials of mongo

Then install using pip:

´´´ pip install . ´´´